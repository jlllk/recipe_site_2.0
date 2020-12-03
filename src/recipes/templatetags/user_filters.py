from django import template

from recipes.models import RecipeFavorite, ShoppingList

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


@register.simple_tag
def set_checkbox_style(tag):
    styles = {
        'Завтрак': 'tags__checkbox_style_orange',
        'Обед': 'tags__checkbox_style_green',
        'Ужин': 'tags__checkbox_style_purple'
    }
    return styles[tag]


@register.simple_tag
def add_query_params(request, tag):

    get_dict = request.GET.copy()

    tags = get_dict.get('tag')
    if tags:
        tag_list = tags.split(',')
        if tag in tag_list:
            tag_list.remove(tag)

            if len(tag_list) == 0:
                get_dict.clear()
                return get_dict.urlencode()
        else:
            tag_list.append(tag)
        tags_string = ','.join(tag_list)
        get_dict['tag'] = tags_string
    else:
        get_dict['tag'] = tag

    return get_dict.urlencode()


@register.simple_tag
def active_checkbox(request, tag):
    tags = request.GET.get('tag')
    if tags:
        tag_list = tags.split(',')
        if tag in tag_list:
            return 'tags__checkbox_active'


@register.simple_tag
def relative_url(value, field_name, urlencode=None):
    """
    Тег генерирует урл с учетом уже имеющихся параметров GET запроса.
    Например, обеспечивает корректную работу пагинатора при включенных
    фильтрах.
    """
    url = '?{}={}'.format(field_name, value)
    if urlencode:
        querystring = urlencode.split('&')
        filtered_querystring = filter(lambda p: p.split('=')[0] != field_name, querystring)
        encoded_querystring = '&'.join(filtered_querystring)
        url = '{}&{}'.format(url, encoded_querystring)
    return url


@register.simple_tag
def already_in_favorites(user, recipe):
    recipe_exists = RecipeFavorite.objects.filter(user=user, recipe=recipe
                                                  ).exists()
    return recipe_exists


@register.simple_tag
def already_in_shopping_list(user, recipe):
    recipe_exists = ShoppingList.objects.filter(user=user, recipe=recipe
                                                ).exists()
    return recipe_exists
