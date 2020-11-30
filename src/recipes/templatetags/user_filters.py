from django import template

register = template.Library()


@register.filter
def addclass(field, css):
    return field.as_widget(attrs={"class": css})


@register.filter
def addcheckboxclass(field, tag):
    tags_styles = {
        'Завтра': 'tags__checkbox_style_orange',
        'Обед': 'tags__checkbox_style_green',
        'Ужин': 'tags__checkbox_style_purple',
    }
    return field.as_widget(attrs={"class": tags_styles[tag]})
