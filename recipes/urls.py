from django.urls import path

from .views import (
    RecipeCreateView,
    RecipeDeleteView,
    RecipeDetailView,
    RecipeUpdateView,
    get_shopping_list
)

urlpatterns = [
    path('<int:pk>/', RecipeDetailView.as_view(), name='recipe_detail'),
    path('create/', RecipeCreateView.as_view(), name='recipe_create'),
    path('<int:pk>/update/', RecipeUpdateView.as_view(), name='recipe_update'),
    path('<int:pk>/delete/', RecipeDeleteView.as_view(), name='recipe_delete'),
    path(
        'ingredients/download/',
        get_shopping_list,
        name='ingredients_download',
    ),
]
