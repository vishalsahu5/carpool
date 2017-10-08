from django.conf.urls import url

from . import views

app_name = 'journeys'

urlpatterns = [
    url(r"^$", views.ListJourneys.as_view(), name="all"),
    url(r"^new/(?P<user_id>\d+)/$", views.create_journey, name="create"),
    url(r"^journeys/(?P<pk>\d+)/$", views.SingleJourney.as_view(), name="single"),
    url(r"^join/(?P<pk>\d+)/$", views.join_journey, name="join"),
    url(r"^leave/(?P<pk>\d+)/$", views.leave_journey, name="leave"),
    url(r"search/$", views.search_journey, name='search'),
]
