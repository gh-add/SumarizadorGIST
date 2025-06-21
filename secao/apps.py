from django.apps import AppConfig


class SecaoConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "secao"

    def ready(self):
        import secao.signals  
