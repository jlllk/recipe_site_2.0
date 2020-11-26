from django.contrib.auth import get_user_model
from django.db import models


User = get_user_model()


class Tag(models.Model):
    """
    Теги для модели Recipe
    """
    title = models.CharField(max_length=100, blank=False, verbose_name='Тег')

    class Meta:
        verbose_name = 'Тег'
        verbose_name_plural = 'Теги'

    def __str__(self):
        return self.title


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
        null=True,
        blank=True,
        verbose_name='Описание'
    )
    tag = models.ManyToManyField(Tag)
    cooking_time = models.SmallIntegerField(
        blank=False,
        verbose_name='Время приготовления',
    )
    pub_date = models.DateTimeField(
        auto_now=True,
        verbose_name='Дата публикации'
    )

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
    name = models.CharField(
        blank=False,
        max_length=120,
        verbose_name='Ингредиент',
    )
    unit = models.CharField(
        blank=False,
        max_length=10,
        verbose_name='Единицы измерения',
    )

    class Meta:
        verbose_name = 'Ингредиент'
        verbose_name_plural = 'Ингредиенты'

    def __str__(self):
        return self.name


class RecipeIngredient(models.Model):
    """
    Модель описывает количество ингредиентов для рецепта.
    """
    recipe = models.ForeignKey(
        Recipe,
        on_delete=models.CASCADE,
        related_name='ingredients_quantity',
        verbose_name='Рецепт',
    )
    ingredient = models.ForeignKey(
        Ingredient,
        on_delete=models.CASCADE,
        related_name='ingredients',
        verbose_name='Ингредиент',
    )
    quantity = models.SmallIntegerField(
        blank=False,
        default=0,
        verbose_name='Количество',
    )

    class Meta:
        verbose_name = 'Количество ингредиента'
        verbose_name_plural = 'Количество ингредиентов'

    def __str__(self):
        return self.ingredient.name


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
        verbose_name='Рецепты',
    )

    class Meta:
        verbose_name = 'Избранное'
        verbose_name_plural = 'Избранные'
        unique_together = ('user', 'recipe')

    def __str__(self):
        return f'Пользователь {self.user} добавил в избранное {self.recipe}'
