from drf_spectacular.utils import extend_schema
from rest_framework import viewsets, mixins, permissions

from ..models import Order
from ..serializers import OrderCreateSerializer, OrderListSerializer


@extend_schema(tags=['Order'])
class OrderViewSet(viewsets.GenericViewSet,
                   mixins.ListModelMixin,
                   mixins.CreateModelMixin,
                   mixins.UpdateModelMixin):
    permission_classes = (permissions.IsAuthenticated,)

    def get_serializer_class(self):
        if self.action == 'list':
            return OrderListSerializer
        return OrderCreateSerializer

    def get_queryset(self):
        return Order.objects.filter(user=self.request.user)
