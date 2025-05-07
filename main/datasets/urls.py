from django.urls import path, include
from rest_framework.routers import DefaultRouter
from main.datasets.views import DatasetTypeViewSet, DatasetColumnViewSet
from main.datasets.views import DatasetViewSet
from main.datasets.views import DatasetTableView

router = DefaultRouter()
router.register(r'types', DatasetTypeViewSet, basename='dataset-types') # type: ignore
router.register(r'columns', DatasetColumnViewSet, basename='dataset-columns') # type: ignore

#-------------------------------------------------------
# Register the base route last 
#-------------------------------------------------------
# This is important because the base route will catch all requests that don't match the above routes
# and will cause the other routes to not be accessible.
# If you want to change the order of the routes, make sure to register the base route last.
# This is a common pattern in Django REST Framework to avoid route conflicts.

router.register(r'', DatasetViewSet, basename='datasets') 

#-------------------------------------------------------

urlpatterns = [
    path('<int:dataset_id>/data/', DatasetTableView.as_view(), name='dataset-data'),
    
    #-------------------------------------------------------
    # Register the base route last 
    #-------------------------------------------------------
    path('', include(router.urls)),
    #-------------------------------------------------------
]