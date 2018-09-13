from django.dispatch import Signal


post_detect_mention = Signal(providing_args=['user_to', 'user_from', 'target'])
