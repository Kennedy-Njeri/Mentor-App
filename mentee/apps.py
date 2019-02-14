from django.apps import AppConfig

class MenteeConfig(AppConfig):
    name = 'mentee'

    def ready(self):
        import mentee.signals