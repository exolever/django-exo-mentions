DEFAULT_TYPE_PATTERN = 'data-mentiontype'
DEFAULT_UUID_PATTERN = 'data-mentionuuid'


class DjangoMentionTestMixins:
    DEFAULT_HTML_PATTERN = DEFAULT_TYPE_PATTERN + '="{}" ' + DEFAULT_UUID_PATTERN + '="{}"'  # noqa

    def tearDown(self):
        super().tearDown()
        from ..registry import _clear_django_mentions_registry
        _clear_django_mentions_registry()
