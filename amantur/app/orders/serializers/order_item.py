from rest_framework import serializers

from products.serializers import ProductListSerializer
from ..models import OrderItem


class OrderItemCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrderItem
        fields = ['product', 'quantity', 'is_free']


class OrderItemListSerializer(serializers.ModelSerializer):
    product = ProductListSerializer()
    
    class Meta:
        model = OrderItem
        fields = ['product', 'quantity', 'price', 'is_free']
