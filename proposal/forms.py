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
        fields = (
            'title', 'brief', 'area', 'document',
            'author1_name', 'author1_email',
            'author2_name', 'author2_email',
            'author3_name', 'author3_email',
            'author4_name', 'author4_email',
            'author5_name', 'author5_email',
        )


class CustomSIPAXProposalForm(forms.ModelForm):
    author1_name = forms.CharField(label=_('Name'), required=False)
    author1_email = forms.EmailField(label=_('Email'), required=False)
    author2_name = forms.CharField(label=_('Name'), required=False)
    author2_email = forms.EmailField(label=_('Email'), required=False)
    author3_name = forms.CharField(label=_('Name'), required=False)
    author3_email = forms.EmailField(label=_('Email'), required=False)

    class Meta:
        model = Proposal
        fields = (
            'title', 'brief', 'area', 'carga_horaria',
            'quantidade_de_vagas', 'institution',
            'ementa', 'objetivos', 'publico',
            'materiais', 'justificativa',
            'author1_name', 'author1_email',
            'author2_name', 'author2_email',
            'author3_name', 'author3_email',
        )
