from django.db.models.signals import post_save

from .signals.views import post_save_model_detect_mentions
from .conf import settings

REGISTRY = {}


def add_model_to_registry(model, field, callback, pattern):
    REGISTRY[model] = {
        'field': field,
        'callback': callback,
        'pattern': pattern,
    }


def connect_model_with_signals(model):
    post_save.connect(post_save_model_detect_mentions, sender=model)


def register(model, field, callback, pattern=None):
    pattern = settings.MENTIONS_DEFAULT_PATTERN if pattern is None else pattern
    add_model_to_registry(model, field, callback, pattern)
    connect_model_with_signals(model)
