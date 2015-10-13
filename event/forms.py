from django import forms

from event.models import Event


class EventForm(forms.ModelForm):
    class Meta:
        exclude = ('created_at', 'is_published', 'is_public')
        model = Event
        widgets = {
            'categories': forms.CheckboxSelectMultiple()
        }
