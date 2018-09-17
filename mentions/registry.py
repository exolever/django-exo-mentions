from django.db.models.signals import post_save

from .signals.views import post_save_model_detect_mentions

REGISTRY = {}


def get_default_pattern():
    return r'class="mention" data-user=[\'"]?([^\'" >]+)'


def add_to_registry(model, field, callback, pattern):
    pattern = get_default_pattern() if pattern is None else pattern

    REGISTRY[model] = {
        'field': field,
        'callback': callback,
        'pattern': pattern,
    }


def connect_signals(model):
    post_save.connect(post_save_model_detect_mentions, sender=model)


def register(model, field, callback, pattern=None):
    add_to_registry(model, field, callback, pattern)
    connect_signals(model)
