from django.apps import AppConfig


class ItemCollectionsConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'review_collections'

    def ready(self):
        import review_collections.signals
