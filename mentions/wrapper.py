import re
import logging

from django.contrib.auth import get_user_model
from django.core.exceptions import ObjectDoesNotExist
from django.conf import settings

from actstream import action


logger = logging.getLogger('users')


class MentionsWrapper:
    pattern = r'class="mention" data-profile=[\'"]?([^\'" >]+)'
    text = None
    user_from = None
    instance = None

    def __init__(self, *args, **kwargs):
        self.text = kwargs.pop('text')
        self.user_from = kwargs.pop('user_from')
        self.instance = kwargs.pop('instance')

    def get_mentions_profiles(self):
        return re.findall(self.pattern, self.text)

    def detect_mentions(self):
        profiles_list_pk = self.get_mentions_profiles()

        if len(profiles_list_pk):
            for profile_pk in profiles_list_pk:
                try:
                    user_to = get_user_model().objects.get(pk=profile_pk)
                    self.do_mention(
                        user_from=self.user_from,
                        user_to=user_to,
                        target=self.instance)
                except ObjectDoesNotExist:
                    logger.warning('{} can not be mentioned by {}'.format(profile_pk, self.user_from))

    def do_mention(self, user_from, user_to, target=None):
        action.send(
            user_from,
            action_object=user_to,
            target=target,
            verb=settings.MENTIONS_VERB)
