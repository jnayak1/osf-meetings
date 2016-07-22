from __future__ import unicode_literals

from django.apps import AppConfig


class MailConfig(AppConfig):
    name = 'mail'

    def ready(self):
        import signals  # noqa
