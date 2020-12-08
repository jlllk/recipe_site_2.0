from django import template

from recipes.models import Follow, RecipeFavorite, ShoppingList

register = template.Library()


@register.filter
def add_class(field, css):
    return field.as_widget(attrs={"class": css})


@register.simple_tag
def change_query_params(request, tag):

    q_dict = request.GET.copy()
    tags = q_dict.getlist('tag')

    if tag in tags:
        tags.remove(tag)
        q_dict.setlist('tag', tags)
    else:
        q_dict.update({'tag': tag})
    return q_dict.urlencode()


@register.simple_tag
def active_checkbox(request, tag):
    tags = request.GET.getlist('tag')
    if tags:
        if tag in tags:
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
        filtered_querystring = filter(
            lambda p: p.split('=')[0] != field_name, querystring
        )
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


@register.simple_tag
def already_following(user, following):
    following = Follow.objects.filter(user=user, following=following).exists()
    return following
