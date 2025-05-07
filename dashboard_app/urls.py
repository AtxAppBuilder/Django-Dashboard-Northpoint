from django.urls import path
from .views import YouTubeAnalyticsView

urlpatterns = [
    path('youtube-analytics/', YouTubeAnalyticsView.as_view(), name='youtube-analytics'),
]