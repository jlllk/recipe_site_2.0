from rest_framework import serializers

from recipes.models import Ingredient, RecipeFavorite


class IngredientSerializer(serializers.ModelSerializer):
    class Meta:
        fields = ('title', 'dimension')
        model = Ingredient


class RecipeFavoriteSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField()

    class Meta:
        fields = ('id',)
        model = RecipeFavorite
