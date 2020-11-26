from django.urls import path

from .views import UserFollowView
from recipes.views import RecipeFavoriteView

urlpatterns = [
    path('follow/', UserFollowView.as_view(), name='user_follow'),
    path('favorite/', RecipeFavoriteView.as_view(), name='recipe_favorite'),
]