

class DjangoMentionTestMixins:

    def tearDown(self):
        super().tearDown()
        from ..registry import _clear_django_mentions_registry, REGISTRY
        _clear_django_mentions_registry()
