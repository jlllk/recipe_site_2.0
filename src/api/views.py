from django.shortcuts import get_object_or_404

from rest_framework import viewsets, filters, mixins, status, generics
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from recipes.models import Ingredient, Recipe, RecipeFavorite, ShoppingList
from recipes.permissions import IsOwner
from users.models import Follow, User

from .serializers import (
    IngredientSerializer,
    RecipeFavoriteSerializer,
    FollowSerializer,
    ShoppingListSerializer,
)


class IngredientViewSet(generics.ListAPIView):
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


class FavoriteDeleteAPIView(generics.DestroyAPIView):
    """
    APIView удаляет рецепты пользователей из списка избранного. Только владелец
    может совершать эту операцию.
    """
    permission_classes = (IsAuthenticated | IsOwner,)

    def get_object(self, pk):
        return get_object_or_404(RecipeFavorite, pk=pk)

    def delete(self, request, pk, **kwargs):
        favorite = self.get_object(pk)
        favorite.delete()
        return Response({'success': True})


class FavoriteCreateAPIView(generics.CreateAPIView):
    """
    Добавление рецепта в список избранного пользователя. Только
    аутентифицированный пользователь может совершать запрос.
    """
    queryset = RecipeFavorite.objects.all()
    serializer_class = RecipeFavoriteSerializer
    permission_classes = (IsAuthenticated,)

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
        Если рецепт уже добавлен в избранное, то сообщить об этом.
        """
        recipe_id = self.request.data.get('id')
        recipe = get_object_or_404(Recipe, id=recipe_id)

        favorite_recipe_exist = RecipeFavorite.objects.filter(
            user=self.request.user,
            recipe=recipe,
        )
        if favorite_recipe_exist:
            return Response(
                {'message': 'Рецепт уже добавлен в список избранного!'},
                status=status.HTTP_400_BAD_REQUEST,
            )

        serializer.save(user=self.request.user, recipe=recipe)


class FollowCreateAPIView(generics.CreateAPIView):
    """
    Оформление подписки на автора. Только аутентифицированный пользователь
    может совершать запрос.
    """
    queryset = Follow.objects.all()
    serializer_class = FollowSerializer
    permission_classes = (IsAuthenticated,)

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
        Метод создает подписку на автора. В процессе полю user
        присваивается текущий пользователь.
        Если подписка уже существует, то сообщить об этом.
        Нельзя подписаться на самого себя.
        """
        user_id = self.request.data.get('id')
        following = get_object_or_404(User, id=user_id)

        if following is self.request.user:
            return Response(
                {'message': 'Нельзя подписаться на самого себя'},
                status=status.HTTP_400_BAD_REQUEST,
            )

        subscription_exist = Follow.objects.filter(
            user=self.request.user,
            following=following,
        )
        if subscription_exist:
            return Response(
                {'message': 'Вы уде подписаны на этого автора!'},
                status=status.HTTP_400_BAD_REQUEST,
            )

        serializer.save(user=self.request.user, following=following)


class FollowDeleteAPIView(generics.DestroyAPIView):
    """
    APIView удаляет подписку на автора. Только владельцы могут удалять свои
    подписки.
    """
    permission_classes = (IsAuthenticated | IsOwner,)

    def get_object(self, pk):
        return get_object_or_404(Follow, pk=pk)

    def delete(self, request, pk, **kwargs):
        following = get_object_or_404(User, pk=pk)
        follow = get_object_or_404(
            Follow,
            user=request.user,
            following=following,
        )
        follow.delete()
        return Response({'success': True})


class ShoppingListCreateAPIView(generics.CreateAPIView):
    """
    Добавление рецепта в список покупок. Только владельцы могут совершать это
    действие.
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
        return Response(data={'success': True}, status=status.HTTP_201_CREATED)

    def perform_create(self, serializer):
        """
        Метод добавляет рецепт в список покупок. В процессе полю user
        присваивается текущий пользователь.
        Если рецепт уже в списке покупок, то сообщить об этом.
        """
        recipe_id = self.request.data.get('id')
        recipe = get_object_or_404(Recipe, id=recipe_id)

        recipe_exist = ShoppingList.objects.filter(
            user=self.request.user,
            recipe=recipe,
        )
        if recipe_exist:
            return Response(
                {'message': 'Рецепт уже в списке покупок!'},
                status=status.HTTP_400_BAD_REQUEST,
            )

        serializer.save(user=self.request.user, recipe=recipe)


class ShoppingListDeleteAPIView(generics.DestroyAPIView):
    """
    APIView удаляет рецепты из списка покупок. Только владельцы могут совершать
    это действие.
    """
    permission_classes = (IsAuthenticated | IsOwner,)

    def get_object(self, pk):
        return get_object_or_404(Recipe, pk=pk)

    def delete(self, request, pk, **kwargs):
        recipe = get_object_or_404(Recipe, pk=pk)
        recipe_in_shopping_list = get_object_or_404(
            ShoppingList,
            user=request.user,
            recipe=recipe,
        )
        recipe_in_shopping_list.delete()
        return Response({'success': True})
