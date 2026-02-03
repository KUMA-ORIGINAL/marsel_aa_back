from rest_framework import serializers

from .category import CategoryProductSerializer
from ..models import Product


class ProductBaseSerializer(serializers.ModelSerializer):
    category = CategoryProductSerializer(read_only=True, many=True)

    class Meta:
        model = Product
        fields = ('id', 'name', 'photo', 'description', 'price', 'category')


class ProductSerializer(ProductBaseSerializer):
    pass


class ProductListSerializer(ProductBaseSerializer):

    class Meta(ProductBaseSerializer.Meta):
        fields = ('id', 'name', 'photo', 'price', 'category')
