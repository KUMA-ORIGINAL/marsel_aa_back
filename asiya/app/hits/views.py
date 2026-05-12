from drf_spectacular.utils import extend_schema
from rest_framework import viewsets

from .models import Hit
from .serializers import HitSerializer


@extend_schema(tags=['Hits'])
class HitViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Hit.objects.filter(is_hidden=False)
    serializer_class = HitSerializer
