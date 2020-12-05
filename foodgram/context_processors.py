from recipes.models import Tag


def tags(request):
    """
    Добавляет в шаблон переменную c тегами.
    """
    return {
        'tags': Tag.objects.all()
    }
