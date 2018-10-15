from django.conf.urls import url, include


urlpatterns = [
    url(r'^mentions/', include('mentions.api.urls', namespace='mentions'))
]
