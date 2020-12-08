import io

from reportlab.lib.units import cm
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfgen import canvas

from .models import Ingredient, RecipeIngredient


def buffered_shopping_list(ingredients_sum):
    """
    Формируем список покупок в буффере.
    """
    buffer = io.BytesIO()
    pdfmetrics.registerFont(TTFont('FreeSans', 'static/fonts/FreeSans.ttf'))
    p = canvas.Canvas(buffer)
    p.setTitle('Список покупок')
    p.setFont('FreeSans', 16)

    text_object = p.beginText(2 * cm, 29.7 * cm - 2 * cm)
    text_object.textLine('Список покупок:')
    text_object.textLine('')

    for number, item in enumerate(ingredients_sum, start=1):
        ingredient_string = (f"{number}. "
                             f"{item['ingredient__title'].capitalize()} - "
                             f"{item['ingredient_sum']} "
                             f"{item['ingredient__dimension']}")

        text_object.textLine(ingredient_string.rstrip())

    p.drawText(text_object)
    p.showPage()
    p.save()
    buffer.seek(0)

    return buffer


def create_ingredients(form, recipe):
    known_ids = []

    # Собираем id полей формы с ингридиентами, которые не относятся к
    # RecipeCreationModelForm.
    for items in form.data.keys():
        if 'nameIngredient' in items:
            name, id = items.split('_')
            known_ids.append(id)

    ingredients_list = []
    for id in known_ids:
        # Создаем экземпляры классов Ingredient и RecipeIngredient на
        # основе данных из формы, используя собранные ранее id в known_ids.
        ingredient, created = Ingredient.objects.get_or_create(
            title=form.data.get(f'nameIngredient_{id}'),
            dimension=form.data.get(f'unitsIngredient_{id}')
        )
        rec_ingredient, created = RecipeIngredient.objects.get_or_create(
            recipe=recipe,
            ingredient=ingredient,
            quantity=form.data.get(f'valueIngredient_{id}')
        )
        ingredients_list.append(rec_ingredient)

    return ingredients_list


def update_list_of_ingredients(updated_ingredients, recipe):
    all_ingredients = RecipeIngredient.objects.filter(recipe=recipe)
    # Удаляем из базы ингридиенты, которые не оказались в списке
    # updated_ingredients, т.е. пользователь удалил их в форме при
    # редактировании рецепта.
    for ingredient in all_ingredients:
        if ingredient not in updated_ingredients:
            ingredient.delete()
