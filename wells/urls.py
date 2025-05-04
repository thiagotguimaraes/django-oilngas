from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import WellViewSet, WellBoundariesViewSet
from .views import WellFullViewSet


router = DefaultRouter()
router.register(r'wells', WellViewSet)
router.register(r'wells-boundaries', WellBoundariesViewSet)
router.register(r'wells-full', WellFullViewSet, basename='wells-full')


urlpatterns = [
    path('', include(router.urls)),
]

