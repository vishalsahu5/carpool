from django.db import models
from django.conf import settings
from django.core.urlresolvers import reverse
from django.contrib.auth import get_user_model
from django import template

# https://docs.djangoproject.com/en/1.11/howto/custom-template-tags/#inclusion-tags
# This is for the in_journey_members check template tag

register = template.Library()

# get the current user model active

User = get_user_model()


class Journey(models.Model):
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='pool_members')
    starting_from = models.CharField(max_length=255)
    going_to = models.CharField(max_length=255)
    description = models.TextField(blank=True, default='')
    members = models.ManyToManyField(User, through="JourneyMember")
    created_at = models.DateTimeField(auto_now=True)
    going_date = models.DateField()
    going_time = models.TimeField()

    def __str__(self):
        return self.created_by.username + "_" + self.starting_from + "-" + self.going_to

    def get_absolute_url(self):
        return reverse("journeys:single")

    def save(self, *args, **kwargs):
        # self.created_by = User
        super().save(*args, **kwargs)

    class Meta:
        ordering = ["created_at"]


class JourneyMember(models.Model):
    journey = models.ForeignKey(Journey, related_name="memberships")
    user = models.ForeignKey(User, related_name='user_journeys')

    def __str__(self):
        return self.user.username

    class Meta:
        unique_together = ("journey", "user")
