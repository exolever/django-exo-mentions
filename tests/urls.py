from django.urls import path, include


urlpatterns = [
    path('api/', include('tests.urls_api', namespace='api')),
]
