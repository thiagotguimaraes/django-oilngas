from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import WellViewSet
from .views import WellFullViewSet
from .views import DatasetTypeViewSet, DatasetColumnViewSet
from .views import DatasetViewSet
from .views import DatasetTableView


router = DefaultRouter()
router.register(r'wells', WellViewSet) # type: ignore
router.register(r'wells-full', WellFullViewSet, basename='wells-full') # type: ignore
router.register(r'dataset-types', DatasetTypeViewSet) # type: ignore
router.register(r'dataset-columns', DatasetColumnViewSet) # type: ignore
router.register(r'datasets', DatasetViewSet) # type: ignore


urlpatterns = [
    path('', include(router.urls)), # type: ignore
    path('datasets/<int:dataset_id>/data/', DatasetTableView.as_view(), name='dataset-data'),

]

