from rest_framework import serializers

from account.models import AdSlide


class AdSlideSerializer(serializers.ModelSerializer):

    class Meta:
        model = AdSlide
        fields = ('title', 'description', 'photo')
