from django.test import TestCase
from django.contrib.auth import get_user_model

from model_mommy import mommy
from unittest.mock import patch

from faker import Faker
from mentions.mixins.mentions_test_mixins import DjangoMentionTestMixins
from mentions.registry import register

from .models import ModelWithCustomDescriptor
from .signals import post_detect_mention_test_callback


fake = Faker()


class TestDjangoMentionSignals(DjangoMentionTestMixins, TestCase):

    def setUp(self):
        super().setUp()
        register(
            ModelWithCustomDescriptor,
            'text',
            post_detect_mention_test_callback,
        )

    @patch('mentions.wrapper.MentionsWrapper.do_mention')
    def test_model_registration_with_multiple_mentions(self, do_mentions_patch):
        # PREPARE DATA
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
        self.assertTrue(do_mentions_patch.called)
        self.assertEqual(do_mentions_patch.call_count, 2)

    @patch('mentions.wrapper.MentionsWrapper.do_mention')
    def test_model_registration_with_no_mentions(self, do_mentions_patch):
        # PREPARE DATA
        user_mentioned = get_user_model().objects.create(username='1')
        description = 'Hello Post'.format(
            user_mentioned.pk, user_mentioned.pk, user_mentioned.first_name)

        # DO ACTION
        ModelWithCustomDescriptor.objects.create(text=description)

        # ASSERTS
        self.assertFalse(do_mentions_patch.called)

    @patch('mentions.wrapper.MentionsWrapper.do_mention')
    def test_user_mentioned_multiple_times_send_one_mention_signal(
            self, do_mentions_patch):

        # PREPARE DATA
        user = mommy.make(
            get_user_model(),
            email=fake.email(),
            first_name=fake.name(),
        )
        description = ' \
            <a class="mention" data-user="{}">@{}</a> \
            <a class="mention" data-user="{}">@{}</a> \
            '.format(user.pk, user.first_name, user.pk, user.first_name)

        # DO ACTION
        ModelWithCustomDescriptor.objects.create(text=description)

        # ASSERTS
        self.assertTrue(do_mentions_patch.called)
        self.assertEqual(do_mentions_patch.call_count, 1)

    def test_update_mentions_at_object(self):
        # PREPARE DATA
        user_1, user_2, user_3 = [mommy.make(
            get_user_model(),
            email=fake.email(),
            first_name=fake.name())
            for _ in range(3)]
        description = ' \
            <a class="mention" data-user="{}">@{}</a> \
            <a class="mention" data-user="{}">@{}</a> \
            '.format(
            user_1.pk, user_2.first_name,
            user_2.pk, user_2.first_name,
        )

        mention_object = ModelWithCustomDescriptor.objects.create(
            text=description)

        # DO ACTION
        with patch('mentions.wrapper.MentionsWrapper.do_mention') as do_mentions_patch:
            description = ' \
                <a class="mention" data-user="{}">@{}</a> \
                <a class="mention" data-user="{}">@{}</a> \
                '.format(
                user_2.pk, user_2.first_name,
                user_3.pk, user_3.first_name,
            )
            mention_object.text = description
            mention_object.save()

            # ASSERTS
            _call, mock_call_params = do_mentions_patch.call_args_list[0]
            self.assertEqual(do_mentions_patch.call_count, 1)
            self.assertEqual(len(do_mentions_patch.call_args_list), 1)
            self.assertEqual(mock_call_params.get('target'), mention_object)
            self.assertEqual(mock_call_params.get('object_pk'), user_3.pk)
