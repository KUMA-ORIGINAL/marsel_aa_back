from rest_framework import serializers

from .models import Hit


class HitSerializer(serializers.ModelSerializer):
    photo = serializers.SerializerMethodField()

    def get_photo(self, obj):
        request = self.context.get('request')
        if obj.photo and request:
            return request.build_absolute_uri(obj.photo.url)
        return obj.photo.url if obj.photo else None

    class Meta:
        model = Hit
        fields = ('id', 'text', 'photo', 'order')
