from django.contrib.auth import get_user_model
from django.conf import settings

from rest_framework import status
from rest_framework.generics import GenericAPIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated

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

    def post(self, request, format=None):
        serializer = self.get_serializer(data=request.data)

        if serializer.is_valid():
            users = get_user_model().objects.filter(
                first_name__icontains=serializer.data.get('search')
            )
            results = [
                {'type_object': 'user',
                 'name': user.first_name,
                 'uuid': user.pk}
                for user in users
            ]

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
