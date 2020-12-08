from django.shortcuts import get_object_or_404
from recipes.models import Follow, Ingredient, RecipeFavorite, ShoppingList, Recipe
from users.models import User
from rest_framework import serializers


class IngredientSerializer(serializers.ModelSerializer):
    class Meta:
        fields = ('title', 'dimension')
        model = Ingredient


class RecipeFavoriteSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField()

    def validate(self, data):
        """
        Нельзя дважды добавить рецепт в список покупок.
        """
        id = data.get('id')
        recipe = get_object_or_404(Recipe, id=id)
        user = self.context['request'].user
        if RecipeFavorite.objects.filter(user=user, recipe=recipe).exists():
            raise serializers.ValidationError({'success': False})
        return data

    class Meta:
        fields = ('id',)
        model = RecipeFavorite


class FollowSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField()

    def validate(self, data):
        """
        Нельзя подписаться на самого себя.
        """
        id = data.get('id')
        following = get_object_or_404(User, id=id)
        user = self.context['request'].user
        if following == user:
            raise serializers.ValidationError({'success': False})
        return data

    class Meta:
        fields = ('id',)
        model = Follow


class ShoppingListSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField()

    def validate(self, data):
        """
        Нельзя дважды добавить рецепт в список покупок.
        """
        id = data.get('id')
        recipe = get_object_or_404(Recipe, id=id)
        user = self.context['request'].user
        if ShoppingList.objects.filter(user=user, recipe=recipe).exists():
            raise serializers.ValidationError({'success': False})
        return data

    class Meta:
        fields = ('id',)
        model = ShoppingList
