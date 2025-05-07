from django.db import models

class YouTubeAnalytics(models.Model):
    platform = models.CharField(max_length=50, default='YouTube')
    date = models.DateField()
    views = models.IntegerField(default=0)
    likes = models.IntegerField(default=0)
    comments = models.IntegerField(default=0)
    channel_id = models.CharField(max_length=255)
    video_id = models.CharField(max_length=100, blank=True)
    live_views = models.IntegerField(default=0)
    impressions = models.IntegerField(default=0)
    avg_watch_seconds = models.IntegerField(default=0)
    subs_gained = models.IntegerField(default=0)
    subs_lost = models.IntegerField(default=0)
    net_subs = models.IntegerField(default=0)
    total_subs = models.IntegerField(default=0)
    ctr = models.FloatField(default=0.0)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.platform} - {self.date}: {self.views} views"

    class Meta:
        unique_together = ('date', 'channel_id', 'video_id')

# class SocialMediaAnalytics(models.Model):
#     platform = models.CharField(max_length=50)  # e.g., 'YouTube', 'Instagram'
#     metric = models.CharField(max_length=100)   # e.g., 'views', 'likes', 'followers'
#     value = models.IntegerField()
#     date = models.DateField()
#     channel_id = models.CharField(max_length=100, blank=True)  # For YouTube or similar IDs

#     def __str__(self):
#         return f"{self.platform} - {self.metric}: {self.value} on {self.date}"