from django.shortcuts import render
from django.views.generic.list import ListView

from .models import Recipe


class RecipeListView(ListView):
    """
    Домашня страница сайта.
    """
    model = Recipe
    paginate_by = 8


