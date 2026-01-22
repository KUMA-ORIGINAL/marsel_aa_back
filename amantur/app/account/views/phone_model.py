from rest_framework import viewsets, mixins

from ..models import PhoneModel
from ..serializers import PhoneModelSerializer


class PhoneModelViewSet(viewsets.GenericViewSet,
                        mixins.ListModelMixin):
    queryset = PhoneModel.objects.all()
    serializer_class = PhoneModelSerializer

