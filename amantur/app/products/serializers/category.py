from rest_framework import serializers
from ..models import Category


class CategorySerializer(serializers.ModelSerializer):
    children = serializers.SerializerMethodField()

    class Meta:
        model = Category
        fields = ('id', 'name', 'children')

    def get_children(self, instance):
        # Получаем все подкатегории
        children = instance.children.all()
        if children.exists():
            return CategorySerializer(children, many=True).data
        return []


class CategoryProductSerializer(serializers.ModelSerializer):

    class Meta:
        model = Category
        fields = ('id', 'name')