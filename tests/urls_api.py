from django.conf.urls import url, include

app_name = 'api'

urlpatterns = [
    url(r'^mentions/', include('exo_mentions.api.urls', namespace='mentions'))
]
