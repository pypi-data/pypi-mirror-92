try:
    VERSION = (
        __import__("pkg_resources")
        .get_distribution("sentry-slack-integration-webhooks")
        .version
    )
except Exception, e:
    VERSION = "unknown"
