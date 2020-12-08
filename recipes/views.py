from django.conf import settings
from django.contrib.auth import get_user_model
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.http import FileResponse
from django.shortcuts import redirect, render
from django.urls import reverse_lazy
from django.views import View
from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView, DeleteView, UpdateView
from django.views.generic.list import ListView, MultipleObjectMixin

from .forms import RecipeCreationModelForm
from .models import (
    Follow,
    Ingredient,
    Recipe,
    RecipeFavorite,
    RecipeIngredient,
    ShoppingList
)
from .utilities import (
    buffered_shopping_list,
    create_ingredients,
    update_list_of_ingredients,
)

User = get_user_model()


class HomePageView(ListView):
    model = Recipe
    paginate_by = settings.PAGINATE_BY

    def get_queryset(self):
        """
        Фильтруем данные в зависимости от набора переданных в урл тэгов.
        """
        qs = super().get_queryset()
        tags = self.request.GET.getlist('tag')
        if tags:
            qs = qs.filter_by_tags(tags)
        return qs


class RecipeDetailView(DetailView):
    model = Recipe


class RecipeCreateView(LoginRequiredMixin, CreateView):
    model = Recipe
    form_class = RecipeCreationModelForm
    template_name = 'recipes/recipe_create.html'

    def form_valid(self, form):
        form.instance.author = self.request.user
        response = super().form_valid(form)
        create_ingredients(form=form, recipe=self.object)
        return response

    def get_success_url(self):
        return reverse_lazy('recipe_detail', kwargs={'pk': self.object.pk})


class RecipeUpdateView(UserPassesTestMixin, UpdateView):
    model = Recipe
    form_class = RecipeCreationModelForm
    template_name = 'recipes/recipe_create.html'

    def test_func(self):
        recipe = self.get_object()
        return self.request.user == recipe.author or self.request.user.is_admin

    def form_valid(self, form):
        response = super().form_valid(form)
        ingredients_list = create_ingredients(form=form, recipe=self.object)
        update_list_of_ingredients(ingredients_list, recipe=self.object)
        return response

    def get_success_url(self):
        return reverse_lazy('recipe_detail', kwargs={'pk': self.object.pk})


class RecipeDeleteView(UserPassesTestMixin, DeleteView):
    """
    Удалять рецепты могут администраторы и авторы.
    """
    model = Recipe
    success_url = reverse_lazy('home_page')

    def test_func(self):
        recipe = self.get_object()
        return self.request.user == recipe.author or self.request.user.is_admin


class RecipeAuthorPageView(DetailView, MultipleObjectMixin):
    model = User
    paginate_by = settings.PAGINATE_BY
    template_name = 'recipes/recipe_author_detail.html'

    def get_context_data(self, **kwargs):
        """
        Добавляем в контекст страницы все рецепты автора отфильтрованные
        по тегам, если они переданы в запросе.
        """
        author_recipes = self.object.recipes.all()
        tags = self.request.GET.getlist('tag')
        if tags:
            author_recipes = author_recipes.filter_by_tags(tags)
        context = super().get_context_data(
            object_list=author_recipes,
            **kwargs,
        )
        return context


class RecipeFavoriteView(LoginRequiredMixin, ListView):
    model = RecipeFavorite
    paginate_by = settings.PAGINATE_BY
    context_object_name = 'favorite'
    template_name = 'recipes/recipe_favorite.html'

    def get_queryset(self):
        """
        Возвращаем либо весь список избранного, либо отфильтрованные по тегам,
        если они переданы в запросе.
        """
        favorite = super().get_queryset()
        favorite = favorite.filter(user=self.request.user)
        tags = self.request.GET.getlist('tag')
        if tags:
            favorite = favorite.filter_by_tags(tags)
        return favorite


class ShoppingListView(LoginRequiredMixin, View):

    def get(self, request, *args, **kwargs):
        shopping_list = ShoppingList.objects.filter(user=request.user)
        context = {'shopping_list': shopping_list}
        return render(
            request,
            'recipes/recipe_shop_list.html',
            context=context,
        )


class UserFollowView(LoginRequiredMixin, ListView):
    model = Follow
    paginate_by = settings.PAGINATE_BY
    template_name = 'users/user_follow.html'

    def get_queryset(self):
        """
        Возвращаем подписки текущего пользователя.
        """
        following = super().get_queryset()
        following = following.filter(user=self.request.user)
        return following


class DownloadShoppingList(View):
    """
    View генерирует список ингредиентов в формате pdf на основе рецептов,
    добавленных в список покупок. Повторяющиеся ингредиенты суммируются.
    """
    def get(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return redirect('login')

        recipe_ids = request.user.shopping_list.get_ids_flat()
        ingredients_sum = RecipeIngredient.objects.ingredients_sum(recipe_ids)
        buffered_list = buffered_shopping_list(ingredients_sum)

        return FileResponse(
            buffered_list,
            as_attachment=True,
            filename='shopping_list.pdf',
        )


def page_not_found(request, exception):
    return render(request, 'misc/404.html', {'path': request.path}, status=404)


def server_error(request):
    return render(request, 'misc/500.html', status=500)
