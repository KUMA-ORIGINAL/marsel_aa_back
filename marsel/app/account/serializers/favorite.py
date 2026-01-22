from django.contrib.auth import get_user_model
from rest_framework import serializers

from products.serializers import ProductListSerializer

User = get_user_model()


class FavoriteListSerializer(serializers.ModelSerializer):
    favorite_products = ProductListSerializer(many=True, read_only=True)

    class Meta:
        model = User
        fields = ('favorite_products',)
