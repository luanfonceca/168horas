from django.contrib import admin

from course.models import Course


class CourseAdmin(admin.ModelAdmin):
    pass

admin.site.register(Course, CourseAdmin)
