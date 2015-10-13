from django import forms

from event.models import Event
from category.models import Category


class EventForm(forms.ModelForm):
    category = forms.ModelChoiceField(
        queryset=Category.objects.all(),
        empty_label=None
    )

    class Meta:
        exclude = ('created_at', 'is_published', 'is_public')
        model = Event
