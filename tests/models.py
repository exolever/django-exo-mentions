from __future__ import unicode_literals, absolute_import

from django.db import models
from django.conf import settings
from django.contrib.auth.models import AbstractUser


class ModelWithCustomDescriptor(models.Model):
    text = models.TextField()
    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='%(app_label)s_%(class)s_related',
        null=True, blank=True,
    )

    class Meta:
        verbose_name = 'TestModel'

    def __str__(self):
        return self.text


class CustomUser(AbstractUser):

    full_name = models.CharField(
        'Full name',
        max_length=255,
        blank=True,
        null=True)
