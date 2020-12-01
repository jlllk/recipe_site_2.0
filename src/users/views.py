from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render
from django.urls import reverse_lazy
from django.views import View
from django.views.generic.list import ListView
from django.views.generic import CreateView


from .forms import CreationForm
from .models import Follow


class SignUpView(CreateView):
    form_class = CreationForm
    success_url = reverse_lazy('login')
    template_name = 'auth/registration.html'


class UserFollowView(LoginRequiredMixin, ListView):
    model = Follow
    paginate_by = 6
    context_object_name = 'following'
    template_name = 'users/user_follow.html'

    def get_queryset(self):
        """
        Возвращаем подписки текущего пользователя.
        """
        following = super().get_queryset()
        following = following.filter(user=self.request.user)
        return following

