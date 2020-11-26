from django.contrib.auth import get_user_model
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render
from django.views import View
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView

from .models import Recipe, RecipeFavorite

User = get_user_model()


class HomePageView(ListView):
    model = Recipe
    paginate_by = 8


class RecipeDetailView(DetailView):
    model = Recipe


class RecipeAuthorPageView(DetailView):
    model = User
    template_name = 'recipes/recipe_author_detail.html'


class RecipeFavoriteView(LoginRequiredMixin, View):

    def get(self, request, *args, **kwargs):
        favorite = RecipeFavorite.objects.filter(user=request.user)
        context = {'favorite': favorite}
        return render(request, 'recipes/recipe_favorite.html', context=context)
