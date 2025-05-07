from django.contrib import admin
from .models import YouTubeAnalytics

@admin.register(YouTubeAnalytics)
class YouTubeAnalyticsAdmin(admin.ModelAdmin):
    list_display = ['date', 'views', 'likes', 'comments', 'total_subs']
    list_filter = ['date', 'channel_id']
    search_fields = ['channel_id', 'video_id']