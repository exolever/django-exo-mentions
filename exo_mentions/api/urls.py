from django.urls import path

from .views import SearchMentionAPIView

app_name = 'mentions'

urlpatterns = [
    path('search/', SearchMentionAPIView.as_view(), name='search'),
]
