from django.contrib import admin

from . import models


# class JourneyMemberInline(admin.TabularInline):
#     model = models.JourneyMember


admin.site.register(models.Journey)
# admin.site.register(models.JourneyMember)
