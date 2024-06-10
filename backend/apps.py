from django.apps import AppConfig

class BackendConfig(AppConfig):
    name = 'backend'

    def ready(self):
        from .scrapper import Scrapper


