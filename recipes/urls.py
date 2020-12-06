from django.urls import path

from .views import (
    RecipeAuthorPageView,
    RecipeCreateView,
    RecipeDeleteView,
    RecipeDetailView,
    RecipeFavoriteView,
    RecipeUpdateView,
    ShoppingListView,
    UserFollowView,
    DownloadShoppingList,
)

urlpatterns = [
    path('<int:pk>/', RecipeDetailView.as_view(), name='recipe_detail'),
    path('create/', RecipeCreateView.as_view(), name='recipe_create'),
    path('<int:pk>/update/', RecipeUpdateView.as_view(), name='recipe_update'),
    path('<int:pk>/delete/', RecipeDeleteView.as_view(), name='recipe_delete'),
    path(
        'ingredients/download/',
        DownloadShoppingList.as_view(),
        name='ingredients_download',
    ),
    path(
        'author/<int:pk>/',
        RecipeAuthorPageView.as_view(),
        name='recipe_author',
    ),
    path('follow/', UserFollowView.as_view(), name='user_follow'),
    path('favorite/', RecipeFavoriteView.as_view(), name='recipe_favorite'),
    path('shop-list/', ShoppingListView.as_view(), name='shopping_list'),
]
