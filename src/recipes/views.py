from django.shortcuts import render
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView

from .models import Recipe


class HomePageView(ListView):
    model = Recipe
    paginate_by = 8


class RecipeDetailView(DetailView):
    model = Recipe
