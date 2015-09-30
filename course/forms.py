from django import forms

from course.models import Course


class CourseForm(forms.ModelForm):
    class Meta:
        exclude = ('created_at',)
        model = Course
