#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
test_django-mentions
------------

Tests for `django-mentions` models module.
"""

from django.test import TestCase
from django.contrib.auth import get_user_model

from mock import patch

from mentions.registry import register

from .signals import post_detect_mention_test_callback
from .models import ModelWithCustomDescriptor


class TestMentions(TestCase):

    def setUp(self):
        pass

    @patch('mentions.wrapper.MentionsWrapper.do_mention')
    def test_model_registration_with_multiple_mentions(self, mocked_handler):
        # PREPARE DATA
        register(ModelWithCustomDescriptor, 'text', post_detect_mention_test_callback)
        user_mentioned_1 = get_user_model().objects.create(username='1')
        user_mentioned_2 = get_user_model().objects.create(username='2')
        description = 'Hi <a class="mention" data-user="{}", '\
            'href="/ecosystem/profile/{}/">@{}</a> and , '\
            '<a class="mention" data-user="{}" href="/ecosystem/profile/{}/">@{}</a>'.format(
                user_mentioned_1.pk, user_mentioned_1.pk, user_mentioned_1.first_name,
                user_mentioned_2.pk, user_mentioned_2.pk, user_mentioned_2.first_name)

        # DO ACTION
        self.instance = ModelWithCustomDescriptor.objects.create(text=description)

        # ASSERTS
        self.assertTrue(mocked_handler.called)
        self.assertEqual(mocked_handler.call_count, 2)

    @patch('mentions.wrapper.MentionsWrapper.do_mention')
    def test_model_registration_with_no_mentions(self, mocked_handler):
        # PREPARE DATA
        register(ModelWithCustomDescriptor, 'text', post_detect_mention_test_callback)
        user_mentioned = get_user_model().objects.create(username='1')
        description = 'Hello Post'.format(
            user_mentioned.pk, user_mentioned.pk, user_mentioned.first_name)

        # DO ACTION
        self.instance = ModelWithCustomDescriptor.objects.create(text=description)

        # ASSERTS
        self.assertFalse(mocked_handler.called)
