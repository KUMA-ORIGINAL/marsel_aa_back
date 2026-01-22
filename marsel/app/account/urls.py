from django.urls import path, include
from rest_framework.routers import DefaultRouter
from djoser.views import UserViewSet

from .views import MeViewSet, AdSlideViewSet, FavoriteProductsViewSet, PhoneModelViewSet, trending_recommendations

router = DefaultRouter()
router.register('ad-slides', AdSlideViewSet)
router.register('favorites', FavoriteProductsViewSet, basename='favorites')
router.register('phone-models', PhoneModelViewSet, basename='phone-models')

urlpatterns = [
    path('', include(router.urls)),
    path('users/me/', MeViewSet.as_view()),
    path('auth/users/', UserViewSet.as_view({'post': 'create'})),
    path('auth/users/activation/', UserViewSet.as_view({'post': 'activation'})),
    path('auth/users/resend_activation/', UserViewSet.as_view({'post': 'resend_activation'})),
    path('auth/users/reset_password/', UserViewSet.as_view({'post': 'reset_password'})),
    path('auth/users/reset_password_confirm/', UserViewSet.as_view({'post': 'reset_password_confirm'})),
    path('trending-recommendations/', trending_recommendations, name='trending-recommendations'),
    path('', include('djoser.urls.jwt')),
]

