from django.conf.urls import url, include


urlpatterns = [
    url(r'^mentions/', include('exo_mentions.api.urls', namespace='mentions'))
]
