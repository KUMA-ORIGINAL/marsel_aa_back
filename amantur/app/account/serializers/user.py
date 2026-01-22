from django.contrib.auth import get_user_model
from rest_framework import serializers

from .phone_model import PhoneModelSerializer

User = get_user_model()


class MeSerializer(serializers.ModelSerializer):
    birthday_discount = serializers.SerializerMethodField()
    phone_model = PhoneModelSerializer()

    class Meta:
        model = User
        fields = ('id', 'email', 'first_name', 'last_name', 'photo', 'birthdate', 'phone_model',
                  'points', 'quantity_of_cases', 'free_cases', 'birthday_discount', 'cluster', 'welcome_discount')

    def get_birthday_discount(self, obj):
        return obj.get_birthday_discount()


class MeUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'email', 'first_name', 'last_name', 'photo', 'phone_model')


class UserListSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ('email', 'first_name', 'last_name', 'photo')
