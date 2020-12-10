from django.shortcuts import get_object_or_404

from recipes.models import (
    Follow,
    Ingredient,
    Recipe,
    RecipeFavorite,
    ShoppingList
)
from rest_framework import serializers
from rest_framework.validators import UniqueTogetherValidator
from users.models import User


class IngredientSerializer(serializers.ModelSerializer):
    class Meta:
        fields = ('title', 'dimension')
        model = Ingredient


class RecipeFavoriteSerializer(serializers.ModelSerializer):

    id = serializers.SlugRelatedField(
        slug_field='id',
        queryset=Recipe.objects.all(),
        source='recipe'
    )
    user = serializers.StringRelatedField(
        default=serializers.CurrentUserDefault(),
        read_only=True
    )

    class Meta:
        model = RecipeFavorite
        fields = ('id', 'user')
        validators = (
            UniqueTogetherValidator(
                queryset=RecipeFavorite.objects.all(),
                fields=('id', 'user')),
        )

    def create(self, validated_data):
        """ Создаётся связь """
        if 'user' not in validated_data:
            validated_data['user'] = self.context['request'].user
        return RecipeFavorite.objects.create(**validated_data)


class FollowSerializer(serializers.ModelSerializer):

    id = serializers.SlugRelatedField(
        slug_field='id',
        queryset=User.objects.all(),
        source='following'
    )
    user = serializers.StringRelatedField(
        default=serializers.CurrentUserDefault(),
        read_only=True
    )

    class Meta:
        model = RecipeFavorite
        fields = ('id', 'user')
        validators = (
            UniqueTogetherValidator(
                queryset=Follow.objects.all(),
                fields=('id', 'user')),
        )

    def create(self, validated_data):
        """ Создаётся связь """
        if 'user' not in validated_data:
            validated_data['user'] = self.context['request'].user
        return Follow.objects.create(**validated_data)


class ShoppingListSerializer(serializers.ModelSerializer):

    id = serializers.SlugRelatedField(
        slug_field='id',
        queryset=Recipe.objects.all(),
        source='recipe'
    )
    user = serializers.StringRelatedField(
        default=serializers.CurrentUserDefault(),
        read_only=True
    )

    class Meta:
        model = ShoppingList
        fields = ('id', 'user')
        validators = (
            UniqueTogetherValidator(
                queryset=ShoppingList.objects.all(),
                fields=('id', 'user')),
        )

    def create(self, validated_data):
        """ Создаётся связь """
        if 'user' not in validated_data:
            validated_data['user'] = self.context['request'].user
        return ShoppingList.objects.create(**validated_data)
