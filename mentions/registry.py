from django.db.models.signals import post_save

from .signals.views import post_save_model_detect_mentions

REGISTRY = {}


def add_model_to_registry(model, field, callback):
    REGISTRY[model] = {
        'field': field,
        'callback': callback
    }


def connect_model_with_signals(model):
    post_save.connect(post_save_model_detect_mentions, sender=model)


def register_model_to_detect_mentions(model, field, callback):
    add_model_to_registry(model, field, callback)
    connect_model_with_signals(model)
