from django.dispatch import receiver
from django.core.signals import request_finished


@receiver(request_finished)
def post_detect_mention_test_callback(sender, **kwargs):
    pass
