from django.conf.urls import url

from . import views

app_name = 'notification'

urlpatterns = [
    url(r"^$", views.ListNotifications.as_view(), name="all"),
    url(r"^(?P<notification_id>\d+)/$", views.SingleNotification.as_view(), name="show"),
    url(r"^delete/(?P<notification_id>\d+)/$", views.delete_notification, name="delete"),
]
