from django import forms

from event.models import Event


class EventForm(forms.ModelForm):
    organizer_confirmation = forms.BooleanField(required=False)

    class Meta:
        exclude = (
            'created_at', 'is_published',
            'is_public', 'created_by',
        )
        model = Event
        widgets = {
            'categories': forms.CheckboxSelectMultiple()
        }
