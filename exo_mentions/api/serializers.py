from django.core.exceptions import ObjectDoesNotExist

from rest_framework import serializers

from ..registry import get_model_class_registered_from_name
from ..exceptions import DjangoMentionException


class SearchMentionSerializer(serializers.Serializer):

    search = serializers.CharField()

    object_type = serializers.CharField()
    object_pk = serializers.CharField()

    def validate_object_type(self, value):
        try:
            get_model_class_registered_from_name(value)
        except DjangoMentionException:
            raise serializers.ValidationError(
                'Mentions is not enabled for <{}> objects.'.format(
                    value
                )
            )

        return value

    def validate_object_pk(self, value):
        try:
            actor = self.context.get('request').user
            mention_context_object_class_name = self.initial_data.get('object_type')

            mention_context_object_class = get_model_class_registered_from_name(
                mention_context_object_class_name)
            mention_context_object = mention_context_object_class.objects.get(pk=value)

            assert mention_context_object.can_mention(actor)

        except DjangoMentionException:
            return value

        except ObjectDoesNotExist:
            raise serializers.ValidationError(
                '<{}> with id {} object does not exist.'.format(
                    mention_context_object_class_name,
                    value,
                )
            )

        except AssertionError:
            raise serializers.ValidationError(
                'You are not able to mention at this <{}> object'.format(
                    mention_context_object_class_name
                )
            )

        return value


class SearchMentionResultsSerializer(serializers.Serializer):
    """
    Data serializer for Mention api search
    """

    type_object = serializers.CharField()
    name = serializers.CharField()
    uuid = serializers.CharField()
