from django.shortcuts import get_object_or_404
from drf_spectacular.utils import extend_schema, extend_schema_view
from rest_framework import viewsets, mixins, status
from rest_framework import permissions
from rest_framework.response import Response

from products.models import Product
from ..serializers import FavoriteListSerializer


@extend_schema(tags=['Favorite products'])
@extend_schema_view(
    list=extend_schema(
        summary='Получение избранных продуктов'
    ),
    retrieve=extend_schema(
        summary='Добавлние и удаление из избранных',
        description='При запросе передается id поста и добавляется в '
                    'избранные, при повторном запросе удаляется из избранных',
    )
)
class FavoriteProductsViewSet(viewsets.GenericViewSet,
                              mixins.RetrieveModelMixin,
                              mixins.ListModelMixin):
    permission_classes = (permissions.IsAuthenticated,)
    serializer_class = FavoriteListSerializer
    lookup_field = 'product_id'

    def get_queryset(self):
        user = self.request.user
        return user.favorite_products.all()

    def retrieve(self, request, *args, **kwargs):
        user = request.user
        article = get_object_or_404(Product, pk=kwargs.get('product_id'))

        if article in user.favorite_products.all():
            user.favorite_products.remove(article)
            return Response({'message': 'Product removed from favorites'},
                            status=status.HTTP_200_OK)
        user.favorite_products.add(article)
        return Response({'message': 'Product added to favorites'},
                        status=status.HTTP_200_OK)

    def list(self, request, *args, **kwargs):
        user = request.user
        serializer = self.serializer_class(user, context={'request': request})
        return Response(serializer.data)
