from rest_framework import viewsets, filters

from recipes.models import Ingredient
from .serializers import IngredientSerializer


class IngredientViewSet(viewsets.ModelViewSet):
    """
    """
    serializer_class = IngredientSerializer

    def get_queryset(self):
        """
        """
        queryset = Ingredient.objects.all()
        text = self.request.query_params.get('query', None)
        if text is not None:
            queryset = queryset.filter(title__icontains=text)
        return queryset
