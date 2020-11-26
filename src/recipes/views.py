from django.contrib.auth import get_user_model
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render
from django.views import View
from django.views.generic.edit import CreateView, UpdateView
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from django.urls import reverse_lazy

from .models import Recipe, RecipeFavorite, ShoppingList
from .forms import RecipeCreationModelForm

User = get_user_model()


class HomePageView(ListView):
    model = Recipe
    paginate_by = 8


class RecipeDetailView(DetailView):
    model = Recipe


class RecipeCreateView(CreateView):
    model = Recipe
    form_class = RecipeCreationModelForm
    template_name = 'recipes/recipe_create.html'


class RecipeUpdateView(UpdateView):
    model = Recipe
    form_class = RecipeCreationModelForm
    template_name = 'recipes/recipe_create.html'

    def get_success_url(self):
        return reverse_lazy('recipe_detail', kwargs={'pk': self.object.pk})


class RecipeAuthorPageView(DetailView):
    model = User
    template_name = 'recipes/recipe_author_detail.html'


class RecipeFavoriteView(LoginRequiredMixin, View):

    def get(self, request, *args, **kwargs):
        favorite = RecipeFavorite.objects.filter(user=request.user)
        context = {'favorite': favorite}
        return render(request, 'recipes/recipe_favorite.html', context=context)


class ShoppingListView(LoginRequiredMixin, View):

    def get(self, request, *args, **kwargs):
        shopping_list = ShoppingList.objects.filter(user=request.user)
        context = {'shopping_list': shopping_list}
        return render(
            request,
            'recipes/recipe_shop_list.html',
            context=context,
        )
