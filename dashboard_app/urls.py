from django.urls import path
from .views import MemberList, EventList

urlpatterns = [
    path('members/', MemberList.as_view(), name='member-list'),
    path('events/', EventList.as_view(), name='event-list'),
]