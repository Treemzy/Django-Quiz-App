from django.apps import AppConfig


class AppquizConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'AppQuiz'

    def ready(self):
        import AppQuiz.signals