from django.apps import AppConfig


class NewsConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'posts'
    verbose_name = 'Новости / Посты'

    def ready(self):
        from . import signals
