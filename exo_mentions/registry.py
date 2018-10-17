from django.db.models.signals import post_save, pre_save
from django.conf import settings

from .exceptions import DjangoMentionException
from .signals.save_signals import (
    post_save_model_detect_mentions,
    pre_save_model_detect_mentions,
)

REGISTRY = {}
DEFAULT_PATTERN = r'(data-mentiontype=(?:[\'|\"][a-zA-Z]*(?:\'|\"))) (data-mentionuuid=(?:[\'|\"][a-zA-Z0-9]*(?:\'|\")))'  # noqa


def get_default_pattern():
    return getattr(settings, 'MENTIONS_PATTERN', DEFAULT_PATTERN)


def _get_key_from_model(model):
    return model.__name__


def _add_to_registry(model, field, callback, pattern):
    pattern = pattern or get_default_pattern()
    model_key = _get_key_from_model(model)

    try:
        REGISTRY[model_key]
        raise DjangoMentionException(
            'Model {} already registered.'.format(model))

    except KeyError:
        REGISTRY[model_key] = {
            'model': model,
            'field': field,
            'callback': callback,
            'pattern': pattern,
        }


def _drop_from_registry(model):
    model_key = _get_key_from_model(model)

    try:
        REGISTRY[model_key]
        del REGISTRY[model_key]

    except KeyError:
        raise DjangoMentionException(
            'Model {} not registered.'.format(model))


def _connect_signals(model):
    pre_save.connect(pre_save_model_detect_mentions, sender=model)
    post_save.connect(post_save_model_detect_mentions, sender=model)


def _disconect_signals(model):
    pre_save.disconnect(pre_save_model_detect_mentions, sender=model)
    post_save.disconnect(post_save_model_detect_mentions, sender=model)


def get_model_registered_from_name(nodel_name, raise_exceptions=True):
    registered_model = None
    try:
        registered_model = REGISTRY[nodel_name]
    except KeyError:
        if raise_exceptions:
            raise DjangoMentionException(
                'Model {} not registered'.format(nodel_name))

    return registered_model


def get_model_registered(model_class, raise_exceptions=True):
    model_key = _get_key_from_model(model_class)
    return get_model_registered_from_name(model_key, raise_exceptions)


def register(model, field, callback, pattern=None, raise_exceptions=False):
    try:
        _add_to_registry(model, field, callback, pattern)
        _connect_signals(model)
    except DjangoMentionException as e:
        if raise_exceptions:
            raise e


def unregister(model, raise_exceptions=False):
    try:
        _drop_from_registry(model)
        _disconect_signals(model)
    except DjangoMentionException as e:
        if raise_exceptions:
            raise e


def _clear_django_mentions_registry():
    """
    ** WARNING **
    Do not use this method if you are not sure about what are you doing
    """
    [unregister(REGISTRY[_].get('model')) for _ in list(REGISTRY.keys())]
