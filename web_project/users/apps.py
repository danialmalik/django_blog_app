from django.apps import AppConfig

from .constants import APP_NAME


class UserAppConfig(AppConfig):
    name = APP_NAME

    def ready(self):
        from . import signals  # load the signals when app is ready
