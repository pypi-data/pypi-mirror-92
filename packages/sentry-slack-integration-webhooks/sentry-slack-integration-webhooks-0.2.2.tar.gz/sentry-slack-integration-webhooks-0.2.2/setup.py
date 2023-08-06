#!/usr/bin/env python
"""
sentry-slack-integration-webhooks
=====================

An extension for Sentry which allows to push events to the slack incoming webhooks.

Project forked from the generic sentry-slack-webhooks plugin.
"""
from setuptools import setup, find_packages


install_requires = [
    "sentry>=5.0.0",
]

setup(
    name="sentry-slack-integration-webhooks",
    version="0.2.2",
    author="Pavel Voropaev",
    author_email="pavel.voropaev@gmail.com",
    description="A Sentry extension which pushes events to the slack incoming webhooks.",
    long_description="A Sentry extension which pushes events to the slack incoming webhooks.",
    license="BSD",
    package_dir={"": "src"},
    packages=find_packages("src"),
    zip_safe=False,
    install_requires=install_requires,
    include_package_data=True,
    entry_points={
        "sentry.apps": ["webhooks = sentry_slack_integration_webhooks", ],
        "sentry.plugins": [
            "webhooks = sentry_slack_integration_webhooks.plugin:SlackWebHooksPlugin"
        ],
    },
    classifiers=[
        "Framework :: Django",
        "Intended Audience :: Developers",
        "Intended Audience :: System Administrators",
        "Operating System :: OS Independent",
        "Topic :: Software Development",
    ],
)
