from recipes.models import Ingredient, RecipeFavorite, ShoppingList
from rest_framework import serializers
from users.models import Follow


class IngredientSerializer(serializers.ModelSerializer):
    class Meta:
        fields = ('title', 'dimension')
        model = Ingredient


class RecipeFavoriteSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField()

    class Meta:
        fields = ('id',)
        model = RecipeFavorite


class FollowSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField()

    class Meta:
        fields = ('id',)
        model = Follow


class ShoppingListSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField()

    class Meta:
        fields = ('id',)
        model = ShoppingList
