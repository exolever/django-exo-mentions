from django.conf.urls import url

from .views import SearchMentionAPIView

urlpatterns = [
    url(r'^search/$', SearchMentionAPIView.as_view(), name='search'),
]
