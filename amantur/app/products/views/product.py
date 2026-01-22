from django_filters.rest_framework import DjangoFilterBackend
from drf_spectacular.utils import extend_schema
from rest_framework import viewsets
from rest_framework.filters import OrderingFilter
from rest_framework.pagination import PageNumberPagination

from ..models import Product
from ..serializers import ProductSerializer, ProductListSerializer

class ProductPagination(PageNumberPagination):
    page_size = 10  # Количество объектов на странице для этого вьюсета
    page_size_query_param = 'page_size'  # Позволяет передавать количество объектов через query параметр
    max_page_size = 100  # Максимальное количество объектов на странице


@extend_schema(tags=['Product'])
class ProductViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Product.objects.filter(is_hidden=False)
    pagination_class = ProductPagination
    filter_backends = (DjangoFilterBackend, OrderingFilter)
    filter_fields = ('category',)
    ordering_fields = ('price', 'name')

    def get_serializer_class(self):
        if self.action == 'list':
            return ProductListSerializer
        return ProductSerializer
