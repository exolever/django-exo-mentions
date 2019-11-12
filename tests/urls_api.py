from django.urls import path, include

app_name = 'api'

urlpatterns = [
    path('mentions/', include('exo_mentions.api.urls', namespace='mentions'))
]
