from drf_spectacular.utils import extend_schema
from rest_framework import viewsets
from rest_framework.pagination import PageNumberPagination

from .models import Hit
from .serializers import HitSerializer


class NoPagination(PageNumberPagination):
    page_size = None


@extend_schema(tags=['Hits'])
class HitViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Hit.objects.filter(is_hidden=False)
    serializer_class = HitSerializer
    pagination_class = NoPagination
