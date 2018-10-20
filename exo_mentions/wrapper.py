import re


from .exceptions import DjangoMentionException


class MentionsWrapper:
    mention_context_object = None
    actor = None
    text = None
    original_text = None
    mentionables_entities = {}
    # callback = None
    pattern = None

    def __init__(self, *args, **kwargs):
        self.mention_context_object = kwargs.pop('mention_context_object')
        self.actor = kwargs.pop('actor')
        self.text = kwargs.pop('text')
        self.original_text = kwargs.pop('original_text')
        self.mentionables_entities = kwargs.pop('mentionables_entities')
        self.pattern = kwargs.pop('pattern')

    def _get_callback(self, model, raise_exceptions=True):
        callback = None
        try:
            mentionable_model = self.mentionables_entities.get(model)
            mentionable_model.get('callback')
        except KeyError:
            if raise_exceptions:
                raise DjangoMentionException(
                    'Model {} is not mentionable inside {} context'.format(
                        self.model,
                        self.mention_context_object,
                    ))

        return callback

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

        return {
            mentionable_entity_type: set(mentions.get(mentionable_entity_type))
            for mentionable_entity_type in mentions.keys()
        }

    def detect_mentions(self):
        mentions = self.get_mentions(self.text)
        self.execute_mentions(mentions)

    def update_mentions(self):
        original_mentions = self.get_mentions(self.original_text)
        mentions = self.get_mentions(self.text)

        deleted_mentions = {}
        new_mentions = {}
        for key in set(list(original_mentions.keys()) + list(mentions.keys())):
            deleted_mentions = set(original_mentions.get(key, [])) - set(mentions.get(key, []))  # noqa
            new_mentions[key] = set(mentions.get(key, [])) - set(original_mentions.get(key, []))

        self.execute_mentions(new_mentions)

    def execute_mentions(self, mentions_dict):
        for mentionable_entity_type in mentions_dict.keys():
            for mentionable_entity_pk in mentions_dict.get(mentionable_entity_type):
                self.do_mention(
                    mentionable_entity_type=mentionable_entity_type,
                    mentionable_entity_pk=int(mentionable_entity_pk),
                )

    def do_mention(self, mentionable_entity_type, mentionable_entity_pk):
        callback = self._get_callback(mentionable_entity_type)
        if callback:
            callback(
                sender=self.mention_context_object.__class__,
                user_from=self.actor,
                object_pk=mentionable_entity_pk,
                target=self.mention_context_object,
            )

    # def do_mention(self, actor, object_pk, target=None):
    #     self.callback(
    #         sender=self.instance.__class__,
    #         user_from=actor,
    #         object_pk=object_pk,
    #         target=target)
