from django.conf.urls import url
from django.contrib.auth import views as auth_views
from . import views

app_name = 'accounts'

urlpatterns = [
    url(r"login/$", auth_views.login, {'template_name': 'accounts/login.html'}, name='login'),
    url(r"logout/$", auth_views.logout, name="logout"),
    url(r"signup/$", views.signup, name="signup"),
    # url(r'profile/(?P<username>[-\w]+)/$', views.profile, name='profile'),
    url(r'profile/$', views.profile, name='profile'),
    url(r'update/$', views.update_profile, name='update'),
]
