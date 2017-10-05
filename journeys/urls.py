from django.conf.urls import url

from . import views

app_name = 'groups'

urlpatterns = [
    url(r"^$", views.ListJourneys.as_view(), name="all"),
    url(r"^new/(?P<user_id>\d+)/$", views.create_journey, name="create"),
    # url(r"^new/$", views.CreateJourney.as_view(), name="create"),
    url(r"^journeys/(?P<pk>\d+)/$", views.SingleJourney.as_view(), name="single"),
    url(r"^join/(?P<pk>\d+)/$", views.JoinJourney.as_view(), name="join"),
    url(r"^leave/(?P<pk>\d+)/$", views.LeaveJourney.as_view(), name="leave"),
]
