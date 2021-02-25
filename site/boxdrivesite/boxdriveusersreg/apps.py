from django.apps import AppConfig


class BoxdriveusersregConfig(AppConfig):
    name = 'boxdriveusersreg'

    def ready(self):
        import boxdriveusersreg.signals