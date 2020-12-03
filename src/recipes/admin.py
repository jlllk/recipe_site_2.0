from django.contrib import admin

from .models import (
    Ingredient,
    Recipe,
    RecipeFavorite,
    RecipeIngredient,
    ShoppingList,
    Tag
)


class RecipeAdmin(admin.ModelAdmin):
    list_display = ('title', 'author', 'recipe_in_favorites')
    search_fields = ('title', 'author', 'tag')
    list_filter = ('tag',)
    empty_value_display = '-пусто-'
    readonly_fields = ('recipe_in_favorites',)

    def recipe_in_favorites(self, instance):
        return instance.favorites.count()

    recipe_in_favorites.short_description = 'В избранном'


class IngredientAdmin(admin.ModelAdmin):
    list_display = ('title', 'dimension')
    search_fields = ('title',)
    empty_value_display = '-пусто-'


class IngredientQuantityAdmin(admin.ModelAdmin):
    list_display = ('ingredient', 'quantity')
    search_fields = ('ingredient',)
    empty_value_display = '-пусто-'


class TagAdmin(admin.ModelAdmin):
    list_display = ('title',)
    search_fields = ('title',)
    empty_value_display = '-пусто-'


class RecipeFavoriteAdmin(admin.ModelAdmin):
    list_display = ('user', 'recipe')
    search_fields = ('user', 'recipe')
    empty_value_display = '-пусто-'


class ShoppingListAdmin(admin.ModelAdmin):
    list_display = ('user', 'recipe')
    search_fields = ('user', 'recipe')
    empty_value_display = '-пусто-'


admin.site.register(Recipe, RecipeAdmin)
admin.site.register(Ingredient, IngredientAdmin)
admin.site.register(RecipeIngredient, IngredientQuantityAdmin)
admin.site.register(RecipeFavorite, RecipeFavoriteAdmin)
admin.site.register(ShoppingList, ShoppingListAdmin)
admin.site.register(Tag, TagAdmin)
