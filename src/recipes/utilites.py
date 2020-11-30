import io

from reportlab.pdfgen import canvas
from reportlab.lib.units import cm
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont


def buffered_shopping_list(ingredients_sum):
    buffer = io.BytesIO()
    pdfmetrics.registerFont(TTFont('FreeSans', 'static/fonts/FreeSans.ttf'))
    p = canvas.Canvas(buffer)
    p.setTitle('Список покупок')
    p.setFont('FreeSans', 16)

    text_object = p.beginText(2 * cm, 29.7 * cm - 2 * cm)
    text_object.textLine('Список покупок:')
    text_object.textLine('')

    for number, item in enumerate(ingredients_sum, start=1):
        ingredient_string = (f"{number}. {item['ingredient__title'].capitalize()} - "
                             f"{item['ingredient_sum']} "
                             f"{item['ingredient__dimension']}")

        text_object.textLine(ingredient_string.rstrip())

    p.drawText(text_object)
    p.showPage()
    p.save()
    buffer.seek(0)

    return buffer