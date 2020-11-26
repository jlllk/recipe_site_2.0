from django.contrib import admin

from .models import Recipe, Ingredient, RecipeIngredient, Tag, RecipeFavorite


class RecipeAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'author')
    search_fields = ('title',)
    empty_value_display = '-пусто-'


class IngredientAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'unit')
    search_fields = ('name',)
    empty_value_display = '-пусто-'


class IngredientQuantityAdmin(admin.ModelAdmin):
    list_display = ('id', 'ingredient', 'quantity')
    search_fields = ('ingredient',)
    empty_value_display = '-пусто-'


class TagAdmin(admin.ModelAdmin):
    list_display = ('id', 'title')
    search_fields = ('title',)
    empty_value_display = '-пусто-'


class RecipeFavoriteAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'recipe')
    search_fields = ('user', 'recipe')
    empty_value_display = '-пусто-'


admin.site.register(Recipe, RecipeAdmin)
admin.site.register(Ingredient, IngredientAdmin)
admin.site.register(RecipeIngredient, IngredientQuantityAdmin)
admin.site.register(RecipeFavorite, RecipeFavoriteAdmin)
admin.site.register(Tag, TagAdmin)
