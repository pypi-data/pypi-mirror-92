#!/usr/bin/env python
"""
sentry-slack-integration-webhooks
=====================

An extension for Sentry which allows to push events to the slack incoming webhooks.

Project forked from the generic sentry-slack-webhooks plugin.
"""
from setuptools import setup, find_packages


tests_require = [
    'nose',
]

install_requires = [
    'ipaddr',
    'sentry>=5.0.0',
]

setup(
    name='sentry-slack-integration-webhooks',
    version='0.1.0',
    author='Pavel Voropaev',
    author_email='pavel.voropaev@gmail.com',
    description='A Sentry extension which pushes events to the slack incoming webhooks.',
    long_description='A Sentry extension which pushes events to the slack incoming webhooks.',
    license='BSD',
    package_dir={'': 'src'},
    packages=find_packages('src'),
    zip_safe=False,
    install_requires=install_requires,
    tests_require=tests_require,
    extras_require={'test': tests_require},
    test_suite='runtests.runtests',
    include_package_data=True,
    entry_points={
       'sentry.apps': [
            'webhooks = sentry_slack_webhooks',
        ],
       'sentry.plugins': [
            'webhooks = sentry_slack_webhooks.plugin:SlackWebHooksPlugin'
        ],
    },
    classifiers=[
        'Framework :: Django',
        'Intended Audience :: Developers',
        'Intended Audience :: System Administrators',
        'Operating System :: OS Independent',
        'Topic :: Software Development'
    ],
)
