from rest_framework import viewsets, mixins
from .models import Well
from .serializers import WellFullSerializer, WellSerializer
from .models import WellBoundaries
from .serializers import WellBoundariesSerializer
from django_filters.rest_framework import DjangoFilterBackend
from .filters import WellFullFilter


class WellViewSet(viewsets.ModelViewSet):
    queryset = Well.objects.all()
    serializer_class = WellSerializer

class WellBoundariesViewSet(viewsets.ModelViewSet):
    queryset = WellBoundaries.objects.all()
    serializer_class = WellBoundariesSerializer

class WellFullViewSet(mixins.ListModelMixin, mixins.RetrieveModelMixin, viewsets.GenericViewSet):
    queryset = Well.objects.all()
    serializer_class = WellFullSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_class = WellFullFilter