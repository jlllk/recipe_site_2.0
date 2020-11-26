from django import forms

from .models import Recipe


class RecipeCreationModelForm(forms.ModelForm):
    class Meta:
        model = Recipe
        fields = (
            'title',
            'tag',
            'cooking_time',
            'description',
            'image',
        )
        widgets = {
            'tag': forms.CheckboxSelectMultiple()
        }