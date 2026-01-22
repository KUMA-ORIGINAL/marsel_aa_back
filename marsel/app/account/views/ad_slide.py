from rest_framework import viewsets, mixins

from account.models import AdSlide
from account.serializers import AdSlideSerializer


class AdSlideViewSet(viewsets.GenericViewSet,
                     mixins.ListModelMixin):
    queryset = AdSlide.objects.all()
    serializer_class = AdSlideSerializer
