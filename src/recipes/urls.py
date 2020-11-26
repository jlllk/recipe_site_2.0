from django.urls import path

from .views import RecipeDetailView

urlpatterns = [
    path('<int:pk>/', RecipeDetailView.as_view(), name='recipe_detail'),
]