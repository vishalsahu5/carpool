from django import template

register = template.Library()


@register.assignment_tag
def all_notifications(user):
    user_obj = user.notification_set.filter(viewed=False)
    return user_obj
