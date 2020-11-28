from django.shortcuts import get_object_or_404

from rest_framework import viewsets, filters, mixins, status, generics
from rest_framework.response import Response

from recipes.models import Ingredient, Recipe, RecipeFavorite
from .serializers import (
    IngredientSerializer,
    RecipeFavoriteSerializer,
)


class IngredientViewSet(generics.ListAPIView):
    serializer_class = IngredientSerializer

    def get_queryset(self):
        queryset = Ingredient.objects.all()
        text = self.request.query_params.get('query', None)
        if text is not None:
            queryset = queryset.filter(title__istartswith=text)
        return queryset


class FavoriteDeleteAPIView(generics.DestroyAPIView):
    """
    APIView удаляет рецепты пользователей из списка избранного.
    """
    def get_object(self, pk):
        return get_object_or_404(RecipeFavorite, pk=pk)

    def delete(self, request, pk, **kwargs):
        favorite = self.get_object(pk)
        favorite.delete()
        return Response({'success': True})


class FavoriteCreateAPIView(generics.CreateAPIView):
    queryset = RecipeFavorite.objects.all()
    serializer_class = RecipeFavoriteSerializer

    def create(self, request, *args, **kwargs):
        """
        Переопределяем метод, чтобы вернуть сообщение {'success': True}.
        """
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        return Response(data={'success': True}, status=status.HTTP_201_CREATED)

    def perform_create(self, serializer):
        """
        Метод создает рецепт в избранное. В процессе полю user
        присваивается текущий пользователь.
        Если рецепт уже добавлен в избранное, то вернуть {'success': True}.
        """
        recipe_id = self.request.data.get('id')
        recipe = get_object_or_404(Recipe, id=recipe_id)

        favorite_recipe_exist = RecipeFavorite.objects.filter(
            user=self.request.user,
            recipe=recipe,
        )
        if favorite_recipe_exist:
            return Response({'success': True}, status=status.HTTP_201_CREATED)

        serializer.save(user=self.request.user, recipe=recipe)


