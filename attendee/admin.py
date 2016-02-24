from django.contrib import admin

from attendee.models import Attendee


class AttendeeAdmin(admin.ModelAdmin):
    pass

admin.site.register(Attendee, AttendeeAdmin)
