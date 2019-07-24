from django.conf.urls import url

from .views import SearchMentionAPIView

app_name = 'mentions'

urlpatterns = [
    url(r'^search/$', SearchMentionAPIView.as_view(), name='search'),
]
