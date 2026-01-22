from rest_framework import serializers
from ..models import PhoneModel


class PhoneModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = PhoneModel
        fields = ('id', 'brand', 'model_name')
