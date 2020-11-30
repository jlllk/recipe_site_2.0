from django.contrib.auth import get_user_model
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render
from django.views import View
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from django.urls import reverse_lazy
from django.http import HttpResponseRedirect

from .models import (
    Recipe,
    RecipeFavorite,
    ShoppingList,
    Ingredient,
    RecipeIngredient,
)
from .forms import RecipeCreationModelForm

User = get_user_model()


class HomePageView(ListView):
    model = Recipe
    paginate_by = 20


class RecipeDetailView(DetailView):
    model = Recipe


class RecipeCreateView(CreateView):
    model = Recipe
    form_class = RecipeCreationModelForm
    template_name = 'recipes/recipe_create.html'

    def form_valid(self, form):
        form.instance.author = self.request.user
        response = super().form_valid(form)

        known_ids = []
        """
        Собираем id полей формы с ингридиентами, которые не относятся к
        RecipeCreationModelForm.
        """
        for items in form.data.keys():
            if 'nameIngredient' in items:
                name, id = items.split('_')
                known_ids.append(id)

        for id in known_ids:
            """
            Создаем экземпляры классов Ingredient и RecipeIngredient на
            основе данных из формы, используя собранные ранее id в known_ids.
            """
            ingredient, created = Ingredient.objects.get_or_create(
                title=form.data.get(f'nameIngredient_{id}'),
                dimension=form.data.get(f'unitsIngredient_{id}')
            )
            RecipeIngredient.objects.create(
                recipe=self.object,
                ingredient=ingredient,
                quantity=form.data.get(f'valueIngredient_{id}')
            )
        return response

    def get_success_url(self):
        return reverse_lazy('recipe_detail', kwargs={'pk': self.object.pk})


class RecipeUpdateView(UpdateView):
    model = Recipe
    form_class = RecipeCreationModelForm
    template_name = 'recipes/recipe_create.html'

    def form_valid(self, form):
        response = super().form_valid(form)

        known_ids = []
        """
        Собираем id полей формы с ингридиентами, которые не относятся к
        RecipeCreationModelForm.
        """
        for items in form.data.keys():
            if 'nameIngredient' in items:
                name, id = items.split('_')
                known_ids.append(id)

        updated_ingredients = []
        for id in known_ids:
            """
            Создаем или получаем экземпляры классов Ingredient и
            RecipeIngredient на основе данных из формы, используя собранные
            ранее id в known_ids.
            """
            ingredient, created = Ingredient.objects.get_or_create(
                title=form.data.get(f'nameIngredient_{id}'),
                dimension=form.data.get(f'unitsIngredient_{id}')
            )
            rec_ingredient, created = RecipeIngredient.objects.get_or_create(
                recipe=self.object,
                ingredient=ingredient,
                quantity=form.data.get(f'valueIngredient_{id}')
            )
            updated_ingredients.append(rec_ingredient)

        all_ingredints = RecipeIngredient.objects.filter(recipe=self.object)
        """
        Удаляем из базы ингридиенты, которые не оказались в списке
        updated_ingredients, т.е. пользователь удалил их в форме при
        редактировании рецепта.
        """
        for ingredient in all_ingredints:
            if ingredient not in updated_ingredients:
                ingredient.delete()
        return response

    def get_success_url(self):
        return reverse_lazy('recipe_detail', kwargs={'pk': self.object.pk})


class RecipeDeleteView(DeleteView):
    model = Recipe
    success_url = reverse_lazy('home_page')


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
