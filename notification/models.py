from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save, m2m_changed
from django.dispatch import receiver
from journeys.models import Journey
from django.shortcuts import get_object_or_404
from django.core.mail import send_mail


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
        SUBJECT = 'Welcome to our site !'
        MESSAGE = 'You have now signed up for our site.'
        FROM = 'noreply.carpoolproject@gmail.com'
        TO = [kwargs.get('instance').email]
        send_mail(SUBJECT, MESSAGE, FROM, TO, fail_silently=True)


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
        SUBJECT = 'User added to your journey'
        MESSAGE = message
        FROM = 'noreply.carpoolproject@gmail.com'
        TO = [instance.created_by.email]
        send_mail(SUBJECT, MESSAGE, FROM, TO, fail_silently=True)
    elif kwargs['action'] == 'post_remove':
        message = '{} is removed from your journey {}'.format(user, instance)
        title = 'A user is removed'
        Notification.objects.create(user=instance.created_by,
                                    title=title,
                                    message=message)
        SUBJECT = 'User is removed from your journey'
        MESSAGE = message
        FROM = 'noreply.carpoolproject@gmail.com'
        TO = [instance.created_by.email]
        send_mail(SUBJECT, MESSAGE, FROM, TO, fail_silently=True)
