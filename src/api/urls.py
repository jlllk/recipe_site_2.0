from django.urls import path, include

from .views import (
    IngredientViewSet,
    FavoriteDeleteAPIView,
    FavoriteCreateAPIView,
    FollowCreateAPIView,
    FollowDeleteAPIView,
    ShoppingListCreateAPIView,
    ShoppingListDeleteAPIView,
)


urlpatterns = [
    path('v1/ingredients/', IngredientViewSet.as_view()),
    path('v1/favorites/', FavoriteCreateAPIView.as_view()),
    path('v1/favorites/<int:pk>/', FavoriteDeleteAPIView.as_view()),
    path('v1/subscriptions/', FollowCreateAPIView.as_view()),
    path('v1/subscriptions/<int:pk>/', FollowDeleteAPIView.as_view()),
    path('v1/purchases/', ShoppingListCreateAPIView.as_view()),
    path('v1/purchases/<int:pk>/', ShoppingListDeleteAPIView.as_view()),
]
