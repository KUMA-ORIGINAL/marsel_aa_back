from django.contrib.auth import get_user_model
from drf_spectacular.utils import extend_schema
from rest_framework import permissions, generics

from ..serializers import MeSerializer, MeUpdateSerializer


User = get_user_model()


@extend_schema(tags=['Users Me'])
class MeViewSet(generics.RetrieveUpdateAPIView):
    queryset = User.objects.all()
    permission_classes  = (permissions.IsAuthenticated,)

    def get_serializer_class(self):
        if self.request.method in ['PUT', 'PATCH']:
            return MeUpdateSerializer
        return MeSerializer

    def get_object(self):
        return self.request.user
