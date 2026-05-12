from rest_framework import serializers

from .category import CategoryProductSerializer
from ..models import Product, ProductPhoto


class ProductPhotoSerializer(serializers.ModelSerializer):
    photo = serializers.SerializerMethodField()

    def get_photo(self, obj):
        request = self.context.get('request')
        if obj.photo and request:
            return request.build_absolute_uri(obj.photo.url)
        return obj.photo.url if obj.photo else None

    class Meta:
        model = ProductPhoto
        fields = ('id', 'photo', 'order')


class ProductBaseSerializer(serializers.ModelSerializer):
    category = CategoryProductSerializer(read_only=True, many=True)
    photo = serializers.SerializerMethodField()

    def get_photo(self, obj):
        request = self.context.get('request')
        if obj.photo and request:
            return request.build_absolute_uri(obj.photo.url)
        return obj.photo.url if obj.photo else None

    class Meta:
        model = Product
        fields = ('id', 'name', 'photo', 'description', 'price', 'category')


class ProductSerializer(ProductBaseSerializer):
    photos = ProductPhotoSerializer(read_only=True, many=True)

    class Meta(ProductBaseSerializer.Meta):
        fields = ('id', 'name', 'photo', 'photos', 'description', 'price', 'category')


class ProductListSerializer(ProductBaseSerializer):

    class Meta(ProductBaseSerializer.Meta):
        fields = ('id', 'name', 'photo', 'price', 'category')
