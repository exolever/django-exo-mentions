from __future__ import unicode_literals, absolute_import

from django.db import models


class ModelWithCustomDescriptor(models.Model):
    text = models.TextField()

    class Meta:
        verbose_name = 'TestModel'

    def __str__(self):
        return self.text
