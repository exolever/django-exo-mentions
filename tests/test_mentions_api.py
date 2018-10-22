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
        [mommy.make(get_user_model(), email=fake.email(), full_name=fake.name())
         for _ in range(5)]
        url = reverse('api:mentions:search')
        last_user = get_user_model().objects.last()
        post_data = {'search': last_user.full_name}

        # DO ACTIONS
        response = self.client.post(url, data=post_data, format='json')

        # ASSERTS
        self.assertTrue(status.is_success(response.status_code))
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0].get('name'), last_user.full_name)

    def test_search_user_api_raise_error(self):
        # PREPARE DATA
        [mommy.make(get_user_model(), email=fake.email(), first_name=fake.name())
         for _ in range(5)]
        url = reverse('api:mentions:search')

        # DO ACTIONS
        response = self.client.post(url, data={}, format='json')

        # ASSERTS
        self.assertTrue(status.is_client_error(response.status_code))
