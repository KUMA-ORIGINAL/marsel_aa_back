from django.urls import path, include
from rest_framework.routers import DefaultRouter

from .views import HitViewSet

router = DefaultRouter()
router.register(r'hits', HitViewSet)

urlpatterns = [
    path('', include(router.urls)),
]
