from datetime import timedelta
from django.utils import timezone
from drf_spectacular.utils import extend_schema
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from products.models import Product, Category
from products.serializers import ProductSerializer


@extend_schema(tags=['trending recommendations'], responses=ProductSerializer(many=True))
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def trending_recommendations(request):
    user = request.user

    if user.cluster != "K3":
        return Response({"detail": "Рекомендации доступны только для кластера К3."}, status=403)

    since = timezone.now() - timedelta(days=60)

    favorite_products = user.favorite_products.all()

    if favorite_products.exists():
        favorite_categories = Category.objects.filter(products__in=favorite_products).distinct()

        products = Product.objects.filter(
            category__in=favorite_categories,
            created_at__gte=since,
            is_hidden=False,
        ).distinct().order_by('-created_at')[:10]
    else:
        products = Product.objects.filter(
            created_at__gte=since,
            is_hidden=False,
        ).order_by('-created_at')[:10]

    serializer = ProductSerializer(products, many=True)
    return Response(serializer.data)
