from django import forms
from django.utils.translation import ugettext as _

from proposal.models import Proposal


class ProposalForm(forms.ModelForm):
    author1_name = forms.CharField(label=_('Name'), required=False)
    author1_email = forms.EmailField(label=_('Email'), required=False)
    author2_name = forms.CharField(label=_('Name'), required=False)
    author2_email = forms.EmailField(label=_('Email'), required=False)
    author3_name = forms.CharField(label=_('Name'), required=False)
    author3_email = forms.EmailField(label=_('Email'), required=False)
    author4_name = forms.CharField(label=_('Name'), required=False)
    author4_email = forms.EmailField(label=_('Email'), required=False)
    author5_name = forms.CharField(label=_('Name'), required=False)
    author5_email = forms.EmailField(label=_('Email'), required=False)

    class Meta:
        model = Proposal
        exclude = (
            'slug', 'created_by', 'activity'
        )
