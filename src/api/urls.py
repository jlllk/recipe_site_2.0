from django.urls import path, include

from rest_framework import routers
from .views import IngredientViewSet


v1_router = routers.DefaultRouter()
v1_router.register('ingredients', IngredientViewSet, basename='ingredients')


urlpatterns = [
    path('v1/', include(v1_router.urls)),
]
