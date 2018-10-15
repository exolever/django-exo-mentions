from django.conf.urls import url, include


urlpatterns = [
    url(r'^api/', include('tests.urls_api', namespace='api')),
]
