import re


class MentionsWrapper:
    instance = None
    user_from = None
    text = None
    original_text = None
    callback = None
    pattern = None

    def __init__(self, *args, **kwargs):
        self.instance = kwargs.pop('instance')
        self.user_from = kwargs.pop('user_from')
        self.text = kwargs.pop('text')
        self.original_text = kwargs.pop('original_text')
        self.callback = kwargs.pop('callback')
        self.pattern = kwargs.pop('pattern')

    def get_mentions(self, text):
        """
        Mentions items from regex findall have this structure -(order matters):
            [('data-mentiontype="User"', 'data-mentionuuid="1"'), ...]
        """
        mentions = {}
        for mention in re.findall(self.pattern, text):
            mention_type = mention[0].split('=')[1][1:-1]
            mention_uuid = mention[1].split('=')[1][1:-1]
            try:
                mentions[mention_type]
            except KeyError:
                mentions[mention_type] = []

            mentions[mention_type].append(mention_uuid)

        return mentions

    def detect_mentions(self):
        mentions = self.get_mentions(self.text)

        for mention_type in mentions.keys():
            for mention_pk in set(mentions.get(mention_type)):
                self.do_mention(
                    user_from=self.user_from,
                    object_pk=int(mention_pk),
                    target=self.instance)

    def update_mentions(self):
        original_mentions = self.get_mentions(self.original_text)
        mentions = self.get_mentions(self.text)

        deleted_mentions = {}
        new_mentions = {}
        for key in list(original_mentions.keys()) + list(mentions.keys()):
            deleted_mentions = set(original_mentions.get(key, [])) - set(mentions.get(key, []))  # noqa
            new_mentions[key] = set(mentions.get(key, [])) - set(original_mentions.get(key, []))

        for mention_type in new_mentions.keys():
            for mention_pk in new_mentions.get(mention_type):
                self.do_mention(
                    user_from=self.user_from,
                    object_pk=int(mention_pk),
                    target=self.instance)

    def do_mention(self, user_from, object_pk, target=None):
        self.callback(
            sender=self.instance.__class__,
            user_from=user_from,
            object_pk=object_pk,
            target=target)
