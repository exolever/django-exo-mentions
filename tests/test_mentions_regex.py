from django.test import TestCase

from exo_mentions.registry import DEFAULT_PATTERN
from exo_mentions.wrapper import MentionsWrapper


class TestMentionsRegex(TestCase):

    def test_wrapper_regex_pattern_detects_html_mentions(self):
        """
        Actual pattern did not match for this cases
            # Mixed order for pattern data attributes
            '<a data-mentionuuid="hola" data-mentiontype="type">test</a>',

        """
        # PREPARE DATA
        wrapper = MentionsWrapper(
            **{
                'instance': 'instance',
                'user_from': 'user_from',
                'text': 'text',
                'original_text': 'original_text',
                'callback': 'callback',
                'pattern': DEFAULT_PATTERN,
            }
        )
        valid_html_tags = [
            '<a data-mentiontype="type" data-mentionuuid="ho324la">test</a>',
            '<span data-mentiontype="type" data-mentionuuid="ho324la">test</span>',     # noqa
            # Differents ' and "
            '<a data-mentiontype=\'test\' data-mentionuuid="hola">test</a>',
            '<a data-mentiontype=\'test\' data-mentionuuid=\'hola\'>test</a>',
            # Differents html attributes between pattern tags
            '<a href="www.test" data-mentiontype="type" data-mentionuuid="hola">test</a>',  # noqa
            '<a data-mentiontype="type" data-mentionuuid="hola" href="www.test">test</a>',  # noqa
            '<a href="www.test" data-mentiontype="type" data-mentionuuid="hola">test</a>',  # noqa
            # Differents data attributes mixed with the pattern ones
            '<a data-false="hola" faked-attribute data-mentiontype="type" data-mentionuuid="hola">test</a>',  # noqa
            '<a data-false="hola" data-mentiontype="type" data-mentionuuid="hola" faked-attribute>test</a>',  # noqa
            '<a faked-attribute data-mentiontype="type" data-mentionuuid="hola" data-false="hola" >test</a>',  # noqa
        ]

        invalid_html_tags = [
            '<a data-mentionuuid="hola" data-mentiontype="type">test</a>',
            '<a data-mentiontype=typ data-mentionuuid="hola">test</a>',
            '<a data-mentiontype="type" data-mentionuuid=hola>test</a>',
            '<a>test</a>',
            '<a data-mentiontype="type" >test</a>',
            '<a data-mentionuuid="hola">test</a>',
        ]

        for case in valid_html_tags:
            self.assertIsNotNone(wrapper.get_mentions(case))

        for case in invalid_html_tags:
            self.assertEqual(wrapper.get_mentions(case), {})
