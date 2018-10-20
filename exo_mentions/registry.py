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


def _add_to_registry(model, field, mentionables_entities, pattern):
    pattern = pattern or get_default_pattern()
    model_key = _get_key_from_model(model)

    try:
        REGISTRY[model_key]
        raise DjangoMentionException(
            'Model {} already registered.'.format(model))

    except KeyError:
        mentionables_entities_processed = {}
        for mentionable_entity_model_class in mentionables_entities.keys():
            mentionable_entity_model_key = _get_key_from_model(mentionable_entity_model_class)
            mentionable_config = mentionables_entities.get(mentionable_entity_model_class)
            model_callback = mentionable_config.get('callback', None)
            model_search_field = mentionable_config.get('search_field', None)

            mentionables_entities_processed[mentionable_entity_model_key] = {}
            mentionables_entities_processed[mentionable_entity_model_key]['callback'] = model_callback
            mentionables_entities_processed[mentionable_entity_model_key]['search_field'] = model_search_field

        REGISTRY[model_key] = {
            'model': model,
            'field': field,
            'mentionables_entities': mentionables_entities_processed,
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


def get_model_registered_from_name(model_name, raise_exceptions=True):
    registered_model = None
    try:
        registered_model = REGISTRY[model_name]
    except KeyError:
        if raise_exceptions:
            raise DjangoMentionException(
                'Model {} not registered'.format(model_name))

    return registered_model


def get_mentionable_objects_for_model(model_name, raise_exceptions=True):
    mentionable_objects = {}
    try:
        mentionable_objects = get_model_registered_from_name(model_name).get(
            'mentionables_entities')
    except DjangoMentionException as e:
        if raise_exceptions:
            raise e

    return mentionable_objects


def get_model_class_registered_from_name(model_name, raise_exceptions=True):
    try:
        return get_model_registered_from_name(model_name).get('model')
    except DjangoMentionException as e:
        if raise_exceptions:
            raise e


def get_model_registered(model_class, raise_exceptions=True):
    model_key = _get_key_from_model(model_class)
    return get_model_registered_from_name(model_key, raise_exceptions)


def register(model, field, mentionables_entities, pattern=None, raise_exceptions=False):
    """
        mentions = [
            {
                model_class: {
                    'callback': method_call_back_user,
                    'search_field': 'first_name'
                },
            },
        ]
    """
    try:
        _add_to_registry(model, field, mentionables_entities, pattern)
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
