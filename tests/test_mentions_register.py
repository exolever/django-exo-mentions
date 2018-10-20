#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
test_django-exo-mentions
------------

Tests for `django-exo-mentions` models module.
"""

from django.apps import apps
from django.contrib.auth import get_user_model
from django.db.models.signals import post_save, pre_save
from django.test import TestCase


from exo_mentions.exceptions import DjangoMentionException
from exo_mentions.mixins.mentions_test_mixins import DjangoMentionTestMixins
from exo_mentions.registry import register, unregister
from exo_mentions.signals.save_signals import (
    post_save_model_detect_mentions,
    pre_save_model_detect_mentions,
)

from .signals import post_detect_mention_test_callback


class TestMentionsRegister(DjangoMentionTestMixins, TestCase):

    def test_model_registration_signals_are_connected_after_register(self):
        # PREPARE DATA
        ModelWithCustomDescriptor = apps.get_model(
            app_label='tests',
            model_name='ModelWithCustomDescriptor',
        )

        # DO ACTION
        register(
            model=ModelWithCustomDescriptor,
            field='text',
            mentionables_entities={
                get_user_model(): {
                    'callback': post_detect_mention_test_callback,
                }
            }
        )

        # ASSERTS
        self.assertTrue(post_save_model_detect_mentions in [_[1]() for _ in post_save.receivers])
        self.assertTrue(pre_save_model_detect_mentions in [_[1]() for _ in pre_save.receivers])

    def test_model_registration_signals_are_not_connected_after_unregister(self):
        # PREPARE DATA
        ModelWithCustomDescriptor = apps.get_model(
            app_label='tests',
            model_name='ModelWithCustomDescriptor',
        )

        # DO ACTION
        unregister(ModelWithCustomDescriptor)

        # ASSERTS
        self.assertFalse(post_save_model_detect_mentions in [_[1]() for _ in post_save.receivers])
        self.assertFalse(pre_save_model_detect_mentions in [_[1]() for _ in pre_save.receivers])

    def test_register_duplicated_model_raise_an_exception(self):
        # PREPARE DATA
        ModelWithCustomDescriptor = apps.get_model(
            app_label='tests',
            model_name='ModelWithCustomDescriptor',
        )

        # PREPARE DATA
        register(
            model=ModelWithCustomDescriptor,
            field='text',
            mentionables_entities={
                get_user_model(): {
                    'callback': post_detect_mention_test_callback,
                }
            }
        )

        # ASSERTS
        with self.assertRaises(DjangoMentionException):
            register(
                model=ModelWithCustomDescriptor,
                field='text',
                mentionables_entities={
                    get_user_model(): {
                        'callback': post_detect_mention_test_callback,
                    }
                },
                raise_exceptions=True,
            )

    def test_unregister_not_registered_model_raise_an_exception(self):
        # PREPARE DATA
        ModelWithCustomDescriptor = apps.get_model(
            app_label='tests',
            model_name='ModelWithCustomDescriptor',
        )

        # ASSERTIONS
        with self.assertRaises(DjangoMentionException):
            unregister(ModelWithCustomDescriptor, raise_exceptions=True)
