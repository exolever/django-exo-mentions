from django.contrib.auth import get_user_model

from rest_framework import status
from rest_framework.generics import GenericAPIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated

from .serializers import SearchMentionResultsSerializer
from .serializers import SearchMentionSerializer


class SearchMentionAPIView(GenericAPIView):

    # permission_classes = (IsAuthenticated, )
    serializer_class = SearchMentionSerializer
    output_serializer = SearchMentionResultsSerializer

    def post(self, request, format=None):
        serializer = self.get_serializer(data=request.data)

        if serializer.is_valid():
            users = get_user_model().objects.filter(
                email__icontains=serializer.data.get('search')
            )
            results = [
                {'type_object': 'user',
                 'name': user.first_name,
                 'uuid': user.pk}
                for user in users
            ]
            output_serializer = self.output_serializer(data=results, many=True)
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
