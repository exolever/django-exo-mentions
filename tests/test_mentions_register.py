#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
test_django-mentions
------------

Tests for `django-mentions` models module.
"""

from django.test import TestCase
from django.db.models.signals import post_save, pre_save


from mentions.exceptions import DjangoMentionException
from mentions.mixins.mentions_test_mixins import DjangoMentionTestMixins
from mentions.registry import register, unregister
from mentions.signals.save_signals import (
    post_save_model_detect_mentions,
    pre_save_model_detect_mentions,
)

from .signals import post_detect_mention_test_callback
from .models import ModelWithCustomDescriptor


class TestMentionsRegister(DjangoMentionTestMixins, TestCase):

    def test_model_registration_signals_are_connected_after_register(self):
        # DO ACTION
        # import ipdb; ipdb.set_trace()
        register(ModelWithCustomDescriptor, 'text', post_detect_mention_test_callback)

        # ASSERTS
        self.assertTrue(post_save_model_detect_mentions in [_[1]() for _ in post_save.receivers])
        self.assertTrue(pre_save_model_detect_mentions in [_[1]() for _ in pre_save.receivers])

    def test_model_registration_signals_are_not_connected_after_unregister(self):
        # DO ACTION
        unregister(ModelWithCustomDescriptor)

        # ASSERTS
        self.assertFalse(post_save_model_detect_mentions in [_[1]() for _ in post_save.receivers])
        self.assertFalse(pre_save_model_detect_mentions in [_[1]() for _ in pre_save.receivers])

    def test_register_duplicated_model_raise_an_exception(self):
        # PREPARE DATA
        register(ModelWithCustomDescriptor, 'text', post_detect_mention_test_callback)

        # ASSERTS
        with self.assertRaises(DjangoMentionException):
            register(
                model=ModelWithCustomDescriptor,
                field='text',
                callback=post_detect_mention_test_callback,
                raise_exceptions=True)

    def test_unregister_not_registered_model_raise_an_exception(self):
        # ASSERTIONS
        with self.assertRaises(DjangoMentionException):
            unregister(ModelWithCustomDescriptor, raise_exceptions=True)
