from rest_framework import viewsets, mixins
from .models import Well
from .serializers import WellFullSerializer, WellSerializer
from django_filters.rest_framework import DjangoFilterBackend
from .filters import WellFullFilter
from .models import DatasetType, DatasetColumn
from .models import Dataset
from .serializers import DatasetTypeSerializer, DatasetColumnSerializer
from .serializers import DatasetSerializer
from .services.dataset_service import create_dataset_table
from rest_framework.exceptions import ValidationError
from rest_framework import status
from rest_framework.response import Response
from rest_framework.exceptions import MethodNotAllowed
from rest_framework.serializers import Serializer

class WellViewSet(viewsets.ModelViewSet):
    queryset = Well.objects.all()
    serializer_class = WellSerializer

class WellFullViewSet(mixins.ListModelMixin, mixins.RetrieveModelMixin, viewsets.GenericViewSet):
    queryset = Well.objects.all()
    serializer_class = WellFullSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_class = WellFullFilter

class DatasetTypeViewSet(viewsets.ModelViewSet):
    queryset = DatasetType.objects.all()
    serializer_class = DatasetTypeSerializer

class DatasetColumnViewSet(viewsets.ModelViewSet):
    queryset = DatasetColumn.objects.all()
    serializer_class = DatasetColumnSerializer

class DatasetViewSet(viewsets.ModelViewSet):
    http_method_names = ['get', 'post', 'delete']
    queryset = Dataset.objects.select_related("dataset_type", "well").all()
    serializer_class = DatasetSerializer

    def perform_create(self, serializer: Serializer):
        dataset_type = serializer.validated_data['dataset_type']
        well = serializer.validated_data['well']

        # Enforce uniqueness before touching the DB
        if Dataset.objects.filter(dataset_type=dataset_type, well=well).exists():
            raise ValidationError("A dataset for this well and dataset type already exists.")
        
        # Create DB record
        instance = serializer.save()

        # Create table
        table_name = create_dataset_table(dataset_type, well.id)
        
        instance.table_name = table_name
        instance.save()

    def destroy(self, request, *args, **kwargs):
        confirm = request.query_params.get("confirm", "false").lower()
        if confirm != "true":
            return Response(
                {"detail": "This action requires ?confirm=true in the query string."},
                status=status.HTTP_400_BAD_REQUEST
            )
        return super().destroy(request, *args, **kwargs)

    def perform_destroy(self, instance):
        # Drop the TimescaleDB table before deleting the record
        from django.db import connection

        with connection.cursor() as cursor:
            cursor.execute(f'DROP TABLE IF EXISTS "{instance.table_name}" CASCADE;')

        instance.delete()

    def update(self, request, *args, **kwargs):
        raise MethodNotAllowed("PUT", detail="Updating datasets is not allowed.")

    def partial_update(self, request, *args, **kwargs):
        raise MethodNotAllowed("PATCH", detail="Partial updating datasets is not allowed.")