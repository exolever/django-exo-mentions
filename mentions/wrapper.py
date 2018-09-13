import re

from .conf import settings


class MentionsWrapper:
    instance = None
    user_from = None
    text = None
    callback = None

    def __init__(self, *args, **kwargs):
        self.instance = kwargs.pop('instance')
        self.user_from = kwargs.pop('user_from')
        self.text = kwargs.pop('text')
        self.callback = kwargs.pop('callback')

    def get_pattern(self):
        try:
            return settings.MENTIONS.get('pattern', settings.MENTIONS_PATTERN)
        except AttributeError:
            return settings.MENTIONS_PATTERN

    def get_mentions_array(self):
        return re.findall(self.get_pattern(), self.text)

    def detect_mentions(self):
        mentions_array = self.get_mentions_array()

        if len(mentions_array):
            for object_pk in mentions_array:
                self.do_mention(
                    user_from=self.user_from,
                    object_pk=object_pk,
                    target=self.instance)

        return mentions_array

    def do_mention(self, user_from, object_pk, target=None):
        self.callback(
            sender=self.instance.__class__,
            user_from=user_from,
            object_pk=object_pk,
            target=target)
