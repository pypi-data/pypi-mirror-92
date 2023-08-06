import sentry_slack_webhooks

import re
import logging
from cgi import escape

from django import forms
from django.utils.translation import ugettext_lazy as _
from urlparse import urlparse

from sentry import http
from sentry.plugins.bases import notify
from sentry.utils import json


LEVEL_TO_COLOR = {
    "debug": "cfd3da",
    "info": "2788ce",
    "warning": "f18500",
    "error": "f43f20",
    "fatal": "d20f2a",
}


class SlackWebHooksOptionsForm(forms.Form):
    webhook = forms.CharField(
        label=_("WebHook URL"),
        widget=forms.TextInput(attrs={"class": "span6"}),
        help_text=_("Ex. https://hooks.slack.com/services/FOO/BAR/BAZ."),
    )
    channel = forms.CharField(
        label=_("Channel"),
        widget=forms.TextInput(attrs={"class": "span6"}),
        help_text=_("Ex. #general"),
    )
    username = forms.CharField(
        label=_("Bot Name"),
        widget=forms.TextInput(attrs={"class": "span6", "placeholder": "Sentry Bot"}),
        help_text=_("Optional user name for the bot that will post the messages."),
    )
    icon = forms.CharField(
        label=_("Bot Icon"),
        widget=forms.TextInput(
            attrs={
                "class": "span6",
                "placeholder": ":ghost:",
                "value": "https://slack.global.ssl.fastly.net/17635/img/services/sentry_48.png",
            }
        ),
        help_text=_("Optional icon emoji or URL to a valid image for the bot."),
    )

    def clean_subdomain(self):
        value = self.cleaned_data.get("subdomain")
        if not re.match("^[a-z0-9_\-]+$", value, re.I):
            raise forms.ValidationError("Invalid subdomain")
        return value

    def clean_channel(self):
        value = self.cleaned_data.get("channel")
        if len(value) and value[0] not in ("@", "#"):
            value = "#" + value
        if not re.match("^[#@][a-z0-9_\-]+$", value, re.I):
            raise forms.ValidationError("Invalid channel")
        return value


class SlackWebHooksPlugin(notify.NotificationPlugin):
    author = "Pavel Voropaev"
    version = sentry_slack_webhooks.VERSION
    description = "Pushes events to the slack incoming webhooks."

    slug = "slack-webhooks"
    title = _("Slack WebHooks")
    conf_title = title
    conf_key = "slack-webhooks"
    project_conf_form = SlackWebHooksOptionsForm
    logger = logging.getLogger("sentry.plugins.slack-webhooks")

    def is_configured(self, project, **kwargs):
        return all((self.get_option(k, project) for k in ("webhook", "channel")))

    def should_notify(self, group, event):
        # Always notify since this is not a per-user notification
        return True

    def color_for_group(self, group):
        return "#" + LEVEL_TO_COLOR.get(group.get_level_display(), "error")

    def notify_users(self, group, event, **kwargs):

        if not self.is_configured(group.project):
            return

        event_dict = dict(event.as_dict())

        webhook = self.get_option("webhook", event.project)
        channel = self.get_option("channel", event.project)
        username = self.get_option("username", event.project)
        icon = self.get_option("icon", event.project)

        project = event.project
        message = group.message_short.encode("utf-8")
        culprit = group.title.encode("utf-8")
        project_name = project.get_full_name().encode("utf-8")

        # title = "%s in %s(%s) <%s|%s>" % (
        #     "New event" if group.times_seen == 1 else "Regression",
        #     escape(project_name.encode("utf-8")),
        #     escape(event_dict.get('platform')),
        #     group.get_absolute_url(),
        #     escape(event.title.encode("utf-8")),
        # )

        title = "<%s|New event in %s>" % (
            group.get_absolute_url(),
            escape(project_name.encode("utf-8").upper()),
        )

        fields = []

        fields.append({"title": "title", "value": escape(event.title.encode("utf-8")), "short": True})
        fields.append({"title": "paltform", "value": escape(event_dict.get('platform')), "short": True})
        fields.append({"title": "level", "value": escape(event_dict.get('level').upper()), "short": True})

        tags = event_dict.get('tags')
        if tags:
            tags_str = ",  ".join(["%s: %s" % (x[0], x[1]) for x in tags])
            fields.append({"title": "tags", "value": tags_str, "short": False})

        if message == culprit:
            culprit = ""
        else:
            fields.append({"title": escape(message), "value": escape(culprit), "short": True})

        escape(event.title.encode("utf-8")),
        if event.location:
            fields.append({"title": "location", "value": event.location, "short": True})

        fields.append({"title": "datetime", "value": event.datetime.isoformat(), "short": True})

        exceptions = event_dict.get("exception", {}).get("values", [])
        if exceptions and isinstance(exceptions, list):
            frames = (exceptions[0] or {}).get("stacktrace", {}).get("frames", [])
            if frames and isinstance(frames, list):
                trace = frames[-1]
                code = "```%s\n\n>%s\n\n%s```" % (
                    "\n".join(trace.get("pre_context", [])),
                    trace["context_line"][1:],
                    "\n".join(trace.get("post_context", [])),
                )
                fields.append(
                    {"title": "trace", "value": code, "short": False,}
                )

        payload = {
            "parse": "none",
            "text": title,
            "channel": channel,
            "attachments": [{"color": self.color_for_group(group), "fields": fields}],
        }

        if username:
            payload["username"] = username

        if icon:
            urlparts = urlparse(icon)
            if urlparts.scheme and urlparts.netloc:
                payload["icon_url"] = icon
            else:
                payload["icon_emoji"] = icon

        data = {"payload": json.dumps(payload)}
        return http.safe_urlopen(webhook, method="POST", data=data)
