from django.conf import settings

from rest_framework import status
from rest_framework.generics import GenericAPIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated

from ..registry import (
    get_model_class_registered_from_name,
    get_mentionable_objects_for_model,
)
from .serializers import SearchMentionSerializer


class SearchMentionAPIView(GenericAPIView):

    permission_classes = (IsAuthenticated, )
    serializer_class = SearchMentionSerializer

    def _get_output_serializer_class(self):
        output_serializer = getattr(
            settings,
            'DJANGO_MENTION_RESULTS_SERIALIZER',
            'exo_mentions.api.serializers'
        )
        return __import__(
            output_serializer,
            fromlist=[''],
        ).SearchMentionResultsSerializer

    def get_object(self, serializer):
        mentioned_model = get_model_class_registered_from_name(
            serializer.initial_data.get('object_type')
        )
        return mentioned_model.objects.get(
            pk=serializer.initial_data.get('object_pk')
        )

    def get_matches(self, serializer, user):
        results = []
        search_string = serializer.data.get('search')
        mentioned_object = self.get_object(serializer)
        mentionable_objects = get_mentionable_objects_for_model(
            serializer.initial_data.get('object_type'),
        )
        for mentionable_object_class_name in mentionable_objects.keys():
            method_name = 'get_mentionables_{}'.format(
                mentionable_object_class_name.lower())
            results += [
                {
                    'type_object': mentionable_object_class_name,
                    'name': getattr(
                        _,
                        mentionable_objects[mentionable_object_class_name].get(
                            'search_field')),
                    'uuid': _.pk
                }
                for _ in getattr(mentioned_object, method_name)(
                    user=user,
                    search_by_field=mentionable_objects[mentionable_object_class_name].get(
                        'search_field'),
                    search_string=search_string,
                )
            ]

        return results

    def post(self, request, format=None):
        serializer = self.get_serializer(data=request.data)
        user = self.request.user

        if serializer.is_valid():
            results = self.get_matches(serializer, user)

            OutputSerializer = self._get_output_serializer_class()
            output_serializer = OutputSerializer(data=results, many=True)
            if output_serializer.is_valid():
                data = output_serializer.data
                status_code = status.HTTP_200_OK
            else:
                data = output_serializer.errors
                status_code = status.HTTP_400_BAD_REQUEST

            response = Response(
                data=data,
                status=status_code,
            )

        else:
            response = Response(
                data=serializer.errors,
                status=status.HTTP_400_BAD_REQUEST)

        return response
