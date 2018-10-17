from rest_framework import serializers


class SearchMentionSerializer(serializers.Serializer):

    search = serializers.CharField()
    type_object = serializers.CharField(required=False)


class SearchMentionResultsSerializer(serializers.Serializer):
    """
    Data serializer for Mention api search
    """

    type_object = serializers.CharField()
    name = serializers.CharField()
    uuid = serializers.CharField()
