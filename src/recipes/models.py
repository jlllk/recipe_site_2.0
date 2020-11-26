from django.contrib.auth import get_user_model
from django.db import models


User = get_user_model()


class Tag(models.TextChoices):
    """
    Теги для модели Recipe
    """
    BREAKFAST = 'завтрак', 'Завтрак'
    LUNCH = 'обед', 'Обед'
    DINNER = 'ужин', 'Ужин'


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
    slug = models.SlugField(unique=True, verbose_name='Слаг')
    image = models.ImageField(upload_to='recipes', verbose_name='Изображение')
    description = models.TextField(
        null=True,
        blank=True,
        verbose_name='Описание'
    )
    ingredient = models.ManyToManyField(
        'IngredientQuantity',
        related_name='recipes',
        verbose_name='Ингредиенты',
    )
    tag = models.CharField(
        choices=Tag.choices,
        default=Tag.BREAKFAST,
        max_length=50,
        verbose_name='Тег',
    )
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


class IngredientQuantity(models.Model):
    """
    Модель описывает количество ингредиентов для рецепта.
    """
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
