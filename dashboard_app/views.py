from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.errors import HttpError
from .models import YouTubeAnalytics
from .serializers import YouTubeAnalyticsSerializer
import google.auth.transport.requests
 
import datetime
import os.path
import pickle

SCOPES = [
    'https://www.googleapis.com/auth/youtube.readonly',
    'https://www.googleapis.com/auth/yt-analytics.readonly',
]

TOKEN_PICKLE = 'token.pickle'
CLIENT_SECRET_FILE = 'client_secret.json'

def get_authenticated_service():
    credentials = None
    if os.path.exists(TOKEN_PICKLE):
        with open(TOKEN_PICKLE, 'rb') as token:
            credentials = pickle.load(token)
    if credentials and credentials.expired and credentials.refresh_token:
        credentials.refresh(google.auth.transport.requests.Request())
    elif not credentials or not credentials.valid:
        flow = InstalledAppFlow.from_client_secrets_file(CLIENT_SECRET_FILE, SCOPES)
        credentials = flow.run_local_server(port=0)
        with open(TOKEN_PICKLE, 'wb') as token:
            pickle.dump(credentials, token)
    youtube_analytics = build('youtubeAnalytics', 'v2', credentials=credentials)
    youtube_data = build('youtube', 'v3', credentials=credentials)
    return youtube_analytics, youtube_data

# Youtube Data API for basic data (0auth not needed)
def get_channel_data(youtube_data, channel_id):
    try:
        request = youtube_data.channels().list(
            part='snippet,statistics',
            id=channel_id
        )
        response = request.execute()
        if 'items' in response and response['items']:
            stats = response['items'][0]['statistics']
            return int(stats.get('subscriberCount', 0))
        else:
            return 0
    except HttpError as e:
        print(f"Error fetching channel stats: {e}")
        return 0
    
def get_current_date():
    today = datetime.datetime.today()
    return today.strftime('%Y-%m-%d')

class YouTubeAnalyticsView(APIView):
    def get(self, request):
        youtube_analytics, youtube_data = get_authenticated_service()
        channel_id = 'UC0d9INTRUo3Ady-PLXlVXKQ' 
        if not channel_id:
            return Response({'error': 'Could not fetch channel ID'}, status=status.HTTP_400_BAD_REQUEST)
        total_subs = get_channel_data(youtube_data, channel_id)

        end_date = datetime.datetime.strptime(get_current_date(), '%Y-%m-%d').date()
        start_date = end_date - datetime.timedelta(days=30)
        try:
            response = youtube_analytics.reports().query(
                ids=f'channel=={channel_id}',
                startDate=start_date.strftime('%Y-%m-%d'),
                endDate=end_date.strftime('%Y-%m-%d'),
                metrics='views,likes,comments,subscribersGained,subscribersLost,averageViewDuration',
                dimensions='day',
            ).execute()

            data_to_store = []
            for row in response.get('rows', []):
                date = row[0]
                views = row[1] or 0
                likes = row[2] or 0
                comments = row[3] or 0
                subs_gained = row[4] or 0
                subs_lost = row[5] or 0
                avg_watch_seconds = row[6] or 0

                analytics_data = YouTubeAnalytics(
                    platform='YouTube',
                    date=date,
                    views=views,
                    likes=likes,
                    comments=comments,
                    channel_id=channel_id,
                    video_id='',
                    impressions=0,
                    avg_watch_seconds=avg_watch_seconds,
                    live_views=0,
                    subs_gained=subs_gained,
                    subs_lost=subs_lost,
                    net_subs=subs_gained - subs_lost,
                    total_subs=total_subs,
                    ctr=0.0 
                )
                data_to_store.append(analytics_data)

            YouTubeAnalytics.objects.bulk_create(data_to_store, ignore_conflicts=True)

            analytics = YouTubeAnalytics.objects.all()
            serializer = YouTubeAnalyticsSerializer(analytics, many=True)
            return Response(serializer.data)
        except HttpError as e:
            print(f"Error fetching YouTube Analytics: {e}")
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)













