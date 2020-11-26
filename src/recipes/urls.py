from django.urls import path

from .views import RecipeDetailView, RecipeAuthorPageView

urlpatterns = [
    path('<int:pk>/', RecipeDetailView.as_view(), name='recipe_detail'),
    path('author/<int:pk>/', RecipeAuthorPageView.as_view(), name='recipe_author'),
]