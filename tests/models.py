from __future__ import unicode_literals, absolute_import

from django.db import models
from django.conf import settings
from django.contrib.auth import get_user_model

from exo_mentions.mixins.mention_model_mixin import MentionModelMixin


class ModelWithCustomDescriptor(MentionModelMixin, models.Model):

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

    def get_mentionables_user(self, user, search_by_field, search_string):
        search_condition = '{}__icontains'.format(search_by_field)
        return get_user_model().objects.filter(
            **{search_condition: search_string}
        )
