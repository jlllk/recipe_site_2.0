from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render
from django.urls import reverse_lazy
from django.views import View
from django.views.generic import CreateView


from .forms import CreationForm
from .models import Follow


class SignUpView(CreateView):
    form_class = CreationForm
    success_url = reverse_lazy('login')
    template_name = 'auth/registration.html'


class UserFollowView(LoginRequiredMixin, View):

    def get(self, request, *args, **kwargs):
        following = Follow.objects.filter(user=request.user)
        context = {'following': following}
        return render(request, 'users/user_follow.html', context=context)
