from django.contrib.auth import get_user_model
from django.shortcuts import render
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView

from .models import Recipe

User = get_user_model()


class HomePageView(ListView):
    model = Recipe
    paginate_by = 8


class RecipeDetailView(DetailView):
    model = Recipe


class RecipeAuthorPageView(DetailView):
    model = User
    template_name = 'recipes/recipe_author_detail.html'
