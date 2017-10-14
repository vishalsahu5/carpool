from django import template

register = template.Library()


@register.filter(name='unread_count')
def unread_count(user):
    count = user.notification_set.filter(viewed=False)
    if len(count) == 0:
        return ""
    return str(len(count))
