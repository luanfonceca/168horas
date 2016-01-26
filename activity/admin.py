from django.contrib import admin

from activity.models import Activity


class ActivityAdmin(admin.ModelAdmin):
    pass

admin.site.register(Activity, ActivityAdmin)
