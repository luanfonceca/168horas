from django import forms

from activity.models import Activity


class ActivityForm(forms.ModelForm):
    organizer_confirmation = forms.BooleanField(required=False)

    class Meta:
        exclude = (
            'created_at', 'is_published',
            'is_public', 'created_by',
        )
        model = Activity
        widgets = {
            'categories': forms.CheckboxSelectMultiple()
        }