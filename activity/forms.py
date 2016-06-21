from django import forms

from activity.models import Activity


class ActivityForm(forms.ModelForm):
    organizer_confirmation = forms.BooleanField(required=False)

    class Meta:
        exclude = (
            'created_at', 'is_published',
            'is_public', 'created_by',
            'attendees',
        )
        model = Activity
        widgets = {
            'categories': forms.CheckboxSelectMultiple(),
            'place_id': forms.HiddenInput()
        }
