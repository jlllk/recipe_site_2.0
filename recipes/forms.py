from django import forms
from django.core.exceptions import ValidationError

from .models import Ingredient, Recipe


class RecipeCreationModelForm(forms.ModelForm):

    def clean(self):
        known_ids = []
        for items in self.data.keys():
            if 'nameIngredient' in items:
                name, id = items.split('_')
                known_ids.append(id)

        for id in known_ids:
            title = self.data.get(f'nameIngredient_{id}'),
            dimension = self.data.get(f'unitsIngredient_{id}')
            print(title, dimension)

            ingredient_exists = Ingredient.objects.filter(
                title=title[0],
                dimension=dimension,
            ).exists()

            print(ingredient_exists)

            if not ingredient_exists:
                raise ValidationError(f'Сохранить ингредиент "{title[0]}" '
                                      f'нельзя! Выберите ингредиент из списка!'
                                      )

    def clean_cooking_time(self):
        data = self.cleaned_data['cooking_time']
        if data < 0:
            raise ValidationError(
                'Время приготовления должно быть положительным числом!',
            )
        return data

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
            'tag': forms.CheckboxSelectMultiple(
                attrs={
                    "class": "tags__checkbox"
                }
            )
        }
