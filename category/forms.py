from django import forms

from category.models import Category


class CategoryForm(forms.ModelForm):
    class Meta:
        exclude = ('created_at', 'courses')
        model = Category
