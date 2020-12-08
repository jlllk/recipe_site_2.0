from django.shortcuts import get_object_or_404

from recipes.models import (
    Follow,
    Ingredient,
    Recipe,
    RecipeFavorite,
    ShoppingList,
)
from recipes.permissions import IsOwner
from rest_framework import generics, status, mixins, viewsets
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from users.models import User

from .serializers import (
    FollowSerializer,
    IngredientSerializer,
    RecipeFavoriteSerializer,
    ShoppingListSerializer
)


class CreateDestroyViewSet(mixins.CreateModelMixin,
                           mixins.DestroyModelMixin,
                           viewsets.GenericViewSet):
    pass


class IngredientAPIView(generics.ListAPIView):
    """
    Возвращает json с отфильтрованным списком ингредиентов по заданным
    параметрам. Используется в форме создания рецепта. Только
    аутентифицированный пользователь может совершать запрос.
    """
    serializer_class = IngredientSerializer
    permission_classes = (IsAuthenticated,)

    def get_queryset(self):
        queryset = Ingredient.objects.all()
        text = self.request.query_params.get('query', None)
        if text is not None:
            queryset = queryset.filter(title__istartswith=text)
        return queryset


class FavoriteViewSet(CreateDestroyViewSet):
    """
    ViewSet добавляет/удаляет рецепты  в/из списка избранного. Только владелец
    может совершать эту операцию.
    """
    queryset = RecipeFavorite.objects.all()
    serializer_class = RecipeFavoriteSerializer
    permission_classes = (IsAuthenticated | IsOwner,)

    def create(self, request, *args, **kwargs):
        """
        Переопределяем метод, чтобы вернуть сообщение {'success': True}.
        """
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        return Response({'success': True}, status=status.HTTP_201_CREATED)

    def perform_create(self, serializer):
        """
        Метод добавляет рецепт в избранное. Полю user присваивается текущий
        пользователь.
        """
        recipe_id = self.request.data.get('id')
        recipe = get_object_or_404(Recipe, id=recipe_id)
        serializer.save(user=self.request.user, recipe=recipe)

    def destroy(self, request, pk, **kwargs):
        favorite = RecipeFavorite.objects.get(pk=pk)
        favorite.delete()
        return Response({'success': True})


class FollowViewSet(CreateDestroyViewSet):
    """
    Создание/удаление подписки на автора. Только аутентифицированный
    пользователь может совершать запрос.
    """
    queryset = Follow.objects.all()
    serializer_class = FollowSerializer
    permission_classes = (IsAuthenticated | IsOwner,)

    def create(self, request, *args, **kwargs):
        """
        Переопределяем метод, чтобы вернуть сообщение {'success': True}.
        """
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        return Response({'success': True}, status=status.HTTP_201_CREATED)

    def perform_create(self, serializer):
        """
        Метод создает подписку на автора. В процессе полю user присваивается
        текущий пользователь.
        """
        user_id = self.request.data.get('id')
        following = get_object_or_404(User, id=user_id)
        serializer.save(user=self.request.user, following=following)

    def destroy(self, request, pk, **kwargs):
        following = get_object_or_404(User, pk=pk)
        follow = Follow.objects.get(user=request.user, following=following)
        follow.delete()
        return Response({'success': True})


class ShoppingListViewSet(CreateDestroyViewSet):
    """
    Добавление/удаление рецепта в список покупок. Только владельцы могут
    совершать это действие.
    """
    queryset = ShoppingList.objects.all()
    serializer_class = ShoppingListSerializer
    permission_classes = (IsAuthenticated | IsOwner,)

    def create(self, request, *args, **kwargs):
        """
        Переопределяем метод, чтобы вернуть сообщение {'success': True}.
        """
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        return Response({'success': True}, status=status.HTTP_201_CREATED)

    def perform_create(self, serializer):
        """
        Метод добавляет рецепт в список покупок. В процессе полю user
        присваивается текущий пользователь.
        """
        recipe_id = self.request.data.get('id')
        recipe = get_object_or_404(Recipe, id=recipe_id)
        serializer.save(user=self.request.user, recipe=recipe)

    def destroy(self, request, pk, **kwargs):
        recipe = Recipe.objects.get(pk=pk)
        recipe_in_shoplist = ShoppingList.objects.get(
            user=request.user,
            recipe=recipe,
        )
        recipe_in_shoplist.delete()
        return Response({'success': True})
