from django import forms

from course.models import Course
from category.models import Category


class CourseForm(forms.ModelForm):
    category = forms.ModelChoiceField(
        queryset=Category.objects.all(),
        empty_label=None
    )

    class Meta:
        exclude = ('created_at',)
        model = Course
