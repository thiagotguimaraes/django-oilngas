from django.urls import path, include
from rest_framework.routers import DefaultRouter
from main.wells.views import WellViewSet
from main.wells.views import WellFullViewSet

router = DefaultRouter()
router.register(r'full', WellFullViewSet, basename='wells-full') # type: ignore


#-------------------------------------------------------
# Register the base route last 
#-------------------------------------------------------
# This is important because the base route will catch all requests that don't match the above routes
# and will cause the other routes to not be accessible.
# If you want to change the order of the routes, make sure to register the base route last.
# This is a common pattern in Django REST Framework to avoid route conflicts.

router.register(r'', WellViewSet, basename='wells')

#-------------------------------------------------------

urlpatterns = [
    #-------------------------------------------------------
    # Register the base route last 
    #-------------------------------------------------------
    path('', include(router.urls)),
    #-------------------------------------------------------
]

