#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
test_django-exo-mentions
------------

Tests for `django-exo-mentions` models module.
"""

from django.contrib.auth import get_user_model
from django.urls import reverse

from faker import Faker
from model_mommy import mommy
from rest_framework import status
from rest_framework.test import APITestCase

from exo_mentions.registry import register

from .models import ModelWithCustomDescriptor
from .signals import post_detect_mention_test_callback


fake = Faker()


class TestAPIMentions(APITestCase):

    def setUp(self):
        user_email = fake.email()
        user_pass = fake.word()
        self.user = mommy.make(
            get_user_model(),
            email=user_email)
        self.user.set_password(user_pass)
        self.user.save()
        self.client.login(
            username=self.user.username,
            password=user_pass)

    def test_search_user_api_find_matchs(self):
        # PREPARE DATA
        [mommy.make(get_user_model(), email=fake.email(), first_name=fake.name())
         for _ in range(5)]

        register(
            model=ModelWithCustomDescriptor,
            field='text',
            mentionables_entities={
                get_user_model(): {
                    'callback': post_detect_mention_test_callback,
                    'search_field': 'first_name',
                }
            }
        )
        url = reverse('api:mentions:search')
        last_user = get_user_model().objects.last()
        mention_object = mommy.make(ModelWithCustomDescriptor)
        post_data = {
            'search': last_user.first_name,
            'object_type': mention_object.__class__.__name__,
            'object_pk': mention_object.pk,
        }

        # DO ACTIONS
        response = self.client.post(url, data=post_data, format='json')

        # ASSERTS
        self.assertTrue(status.is_success(response.status_code))
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0].get('name'), last_user.first_name)

    def test_search_user_api_incorrect_data_raise_error(self):
        # PREPARE DATA
        [mommy.make(get_user_model(), email=fake.email(), first_name=fake.name())
         for _ in range(5)]

        mention_object = mommy.make(ModelWithCustomDescriptor)
        register(
            model=ModelWithCustomDescriptor,
            field='text',
            mentionables_entities={
                get_user_model(): {
                    'callback': post_detect_mention_test_callback,
                }
            }
        )
        url = reverse('api:mentions:search')

        test_cases = [
            {
                'data': {},
                'test_result': '',
            },
            {
                'data': {
                    'search': fake.word(),
                },
            },
            {
                'data': {
                    'search': fake.word(),
                    'object_type': fake.word(),
                },
            },
            {
                'data': {
                    'search': fake.word(),
                    'object_type': fake.word(),
                    'object_pk': fake.numerify(),
                },
            },
            {
                'data': {
                    'search': fake.word(),
                    'object_type': mention_object.__class__.__name__,
                    'object_pk': fake.numerify(),
                },
            },
        ]

        # DO ACTIONS
        for test_case in test_cases:
            response = self.client.post(url, data=test_case.get('data'), format='json')

            # ASSERTS
            self.assertTrue(status.is_client_error(response.status_code))
