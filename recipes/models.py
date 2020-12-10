from django.contrib.auth import get_user_model
from django.db import models
from django.db.models import Sum

User = get_user_model()


class TagColor(models.TextChoices):
    DEFAULT = '---'
    ORANGE = 'orange'
    GREEN = 'green'
    PURPLE = 'purple'


class Tag(models.Model):
    """
    Теги для модели Recipe
    """
    title = models.CharField(max_length=100, blank=False, verbose_name='Тег')
    color = models.CharField(
        max_length=10,
        choices=TagColor.choices,
        default=TagColor.DEFAULT,
        verbose_name='Цвет',
    )

    class Meta:
        verbose_name = 'Тег'
        verbose_name_plural = 'Теги'
        ordering = ('id',)

    def __str__(self):
        return self.title


class RecipeQuerySet(models.QuerySet):
    def filter_by_tags(self, tags):
        return self.filter(tag__title__in=tags).distinct()


class Recipe(models.Model):
    """
    Модель описывает рецепты.
    """
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='recipes',
        verbose_name='Автор',
    )
    title = models.CharField(max_length=200, verbose_name='Название')
    image = models.ImageField(upload_to='recipes', verbose_name='Изображение')
    description = models.TextField(
        blank=False,
        verbose_name='Описание'
    )
    tag = models.ManyToManyField(Tag, blank=False, related_name='recipes')
    cooking_time = models.PositiveSmallIntegerField(
        blank=False,
        verbose_name='Время приготовления',
    )
    pub_date = models.DateTimeField(
        auto_now_add=True,
        verbose_name='Дата публикации'
    )
    objects = RecipeQuerySet.as_manager()

    class Meta:
        verbose_name = 'Рецепт'
        verbose_name_plural = 'Рецепты'
        ordering = ['-pub_date']

    def __str__(self):
        return self.title


class Ingredient(models.Model):
    """
    Модель описывает ингредиенты для рецепта.
    """
    title = models.CharField(
        blank=False,
        max_length=120,
        verbose_name='Ингредиент',
    )
    dimension = models.CharField(
        blank=False,
        max_length=10,
        verbose_name='Единицы измерения',
    )

    class Meta:
        verbose_name = 'Ингредиент'
        verbose_name_plural = 'Ингредиенты'

    def __str__(self):
        return self.title


class RecipeIngredientQuerySet(models.QuerySet):
    def ingredients_sum(self, ids_list):
        return self.filter(
            recipe_id__in=ids_list
        ).values(
            'ingredient__title',
            'ingredient__dimension',
        ).annotate(
            ingredient_sum=Sum('quantity'),
        ).order_by('ingredient__title')


class RecipeIngredient(models.Model):
    """
    Модель описывает количество ингредиентов для рецепта.
    """
    recipe = models.ForeignKey(
        Recipe,
        on_delete=models.CASCADE,
        related_name='ingredients',
        verbose_name='Рецепт',
    )
    ingredient = models.ForeignKey(
        Ingredient,
        on_delete=models.CASCADE,
        related_name='ingredients',
        verbose_name='Ингредиент',
    )
    quantity = models.SmallIntegerField(
        null=True,
        blank=True,
        default=0,
        verbose_name='Количество',
    )
    objects = RecipeIngredientQuerySet.as_manager()

    class Meta:
        verbose_name = 'Количество ингредиента'
        verbose_name_plural = 'Количество ингредиентов'
        unique_together = ('recipe', 'ingredient')

    def __str__(self):
        return self.ingredient.title


class RecipeFavoriteQuerySet(models.QuerySet):
    def filter_by_tags(self, tags):
        return self.filter(recipe__tag__title__in=tags).distinct()


class RecipeFavorite(models.Model):
    """
    Модель описывает избранные рецепты пользователя.
    """
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='favorites',
        verbose_name='Пользователь',
    )
    recipe = models.ForeignKey(
        Recipe,
        on_delete=models.CASCADE,
        related_name='favorites',
        verbose_name='Рецепт',
    )

    objects = RecipeFavoriteQuerySet.as_manager()

    class Meta:
        verbose_name = 'Избранное'
        verbose_name_plural = 'Избранные'
        unique_together = ('user', 'recipe')

    def __str__(self):
        return f'Пользователь {self.user} добавил в избранное {self.recipe}'


class ShoppingListQuerySet(models.QuerySet):
    def get_ids_flat(self):
        return self.values_list('recipe', flat=True)


class ShoppingList(models.Model):
    """
    Модель описывает список покупок пользователя.
    """
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='shopping_list',
        verbose_name='Пользователь',
    )
    recipe = models.ForeignKey(
        Recipe,
        on_delete=models.CASCADE,
        related_name='shopping_list',
        verbose_name='Рецепт',
    )

    objects = ShoppingListQuerySet.as_manager()

    class Meta:
        verbose_name = 'Список покупок'
        verbose_name_plural = 'Списки покупок'
        unique_together = ('user', 'recipe')

    def __str__(self):
        return (f'Пользователь {self.user} добавил в список покупок'
                f'{self.recipe}')


class Follow(models.Model):
    """
    Модель описывает подписки на авторов.
    """
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='follower'
    )
    following = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='following'
    )

    class Meta:
        verbose_name = 'Подписка'
        verbose_name_plural = 'Подписки'
        unique_together = ('user', 'following')
        ordering = ['-id']

    def __str__(self):
        return f'Пользователь {self.user} подписан на {self.following}'
