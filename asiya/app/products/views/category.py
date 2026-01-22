from drf_spectacular.utils import extend_schema
from rest_framework import viewsets

from products.models import Category
from products.serializers import CategorySerializer

@extend_schema(tags=['Category'])
class CategoryViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Category.objects.filter(parent__isnull=True)
    serializer_class = CategorySerializer
