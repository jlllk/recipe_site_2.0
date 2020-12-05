from django.urls import path

from recipes.views import (
    RecipeAuthorPageView,
    RecipeFavoriteView,
    ShoppingListView
)

from .views import UserFollowView

urlpatterns = [
    path('<int:pk>/', RecipeAuthorPageView.as_view(), name='recipe_author'),
    path('follow/', UserFollowView.as_view(), name='user_follow'),
    path('favorite/', RecipeFavoriteView.as_view(), name='recipe_favorite'),
    path('shop-list/', ShoppingListView.as_view(), name='shopping_list'),
]
