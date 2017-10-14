from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save, m2m_changed
from django.dispatch import receiver
from journeys.models import Journey
from django.shortcuts import get_object_or_404


class Notification(models.Model):
    title = models.CharField(max_length=256)
    message = models.TextField()
    viewed = models.BooleanField(default=False)
    user = models.ForeignKey(User)

    def __str__(self):
        return self.title


@receiver(post_save, sender=User)
def create_welcome_message(sender, **kwargs):
    if kwargs.get('created', False):
        Notification.objects.create(user=kwargs.get('instance'),
                                    title='Welcome to our site',
                                    message='Thanks for signing up!')


@receiver(m2m_changed, sender=Journey.members.through)
def journey_members_changed_message(sender, **kwargs):
    instance = kwargs.pop('instance', None)
    (pk,) = kwargs['pk_set']
    user = get_object_or_404(User, pk=pk)
    if kwargs['action'] == 'post_add':
        message = '{} is added to your journey {}'.format(user, instance)
        title = 'A new user is added'
        Notification.objects.create(user=instance.created_by,
                                    title=title,
                                    message=message)
    elif kwargs['action'] == 'post_remove':
        message = '{} is removed from your journey {}'.format(user, instance)
        title = 'A user is removed'
        Notification.objects.create(user=instance.created_by,
                                    title=title,
                                    message=message)
