from rest_framework import serializers
from .models import YouTubeAnalytics

class YouTubeAnalyticsSerializer(serializers.ModelSerializer):
    class Meta:
        model = YouTubeAnalytics
        fields = [
            'id', 'platform', 'date', 'views', 'likes', 'comments',
            'channel_id', 'video_id', 'avg_watch_seconds', 'subs_gained', 
            'subs_lost', 'net_subs','total_subs','created_at'
        ]