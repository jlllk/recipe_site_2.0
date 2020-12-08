from django.urls import path, include

from rest_framework.routers import DefaultRouter

from .views import (
    FavoriteViewSet,
    FollowViewSet,
    IngredientAPIView,
    ShoppingListViewSet,
)

v1_router = DefaultRouter()

v1_router.register('favorites', FavoriteViewSet, 'favorites')
v1_router.register('subscriptions', FollowViewSet, 'subscriptions')
v1_router.register('purchases', ShoppingListViewSet, 'purchases')

urlpatterns = [
    path('v1/ingredients/', IngredientAPIView.as_view()),
    path('v1/', include(v1_router.urls)),
]
