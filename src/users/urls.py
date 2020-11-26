from django.urls import path

from .views import UserFollowView

urlpatterns = [
    path('follow/', UserFollowView.as_view(), name='user_follow'),
]