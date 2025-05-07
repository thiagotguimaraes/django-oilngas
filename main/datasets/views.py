from rest_framework import viewsets
from rest_framework.views import APIView
from main.datasets.models import DatasetType, DatasetColumn
from main.datasets.models import Dataset
from main.datasets.serializers import DatasetTypeSerializer, DatasetColumnSerializer
from main.datasets.serializers import DatasetSerializer
from main.datasets.services.dataset_service import create_dataset_table
from rest_framework.exceptions import ValidationError
from rest_framework import status
from rest_framework.response import Response
from rest_framework.exceptions import MethodNotAllowed
from django.db import connection, transaction

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

    def perform_create(self, serializer):
        dataset_type: DatasetTypeSerializer = serializer.validated_data['dataset_type']
        well = serializer.validated_data['well']

        # Enforce uniqueness before touching the DB
        if Dataset.objects.filter(dataset_type=dataset_type, well=well).exists():
            raise ValidationError("A dataset for this well and dataset type already exists.")
        
        # Use a transaction to ensure atomicity
        with transaction.atomic():
            # Create DB record
            instance = serializer.save()

            # Create table
            try:
                table_name = create_dataset_table(dataset_type, well.id)
            except Exception as e:
                # If table creation fails, rollback the transaction
                raise ValidationError(f"Failed to create table: {str(e)}")
            
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

        # Use a transaction to ensure atomicity
        with transaction.atomic():
            try:
                with connection.cursor() as cursor:
                    cursor.execute(f'DROP TABLE IF EXISTS "{instance.table_name}" CASCADE;')
            except Exception as e:
                # If table drop fails, rollback the transaction
                raise ValidationError(f"Failed to drop table: {str(e)}")

        instance.delete()

    def update(self, request, *args, **kwargs):
        raise MethodNotAllowed("PUT", detail="Updating datasets is not allowed.")

    def partial_update(self, request, *args, **kwargs):
        raise MethodNotAllowed("PATCH", detail="Partial updating datasets is not allowed.")
    

class DatasetTableView(APIView):
    """
    API View to perform CRUD operations on the SQL table specified in Dataset.table_name.
    """

    def get(self, request, dataset_id):
        """
        Retrieve rows from the dataset's table with optional filtering by start_ms and end_ms.
        """
        start_ms = request.query_params.get('start_ms')
        end_ms = request.query_params.get('end_ms')

        # Get the dataset and its table name
        try:
            dataset = Dataset.objects.get(id=dataset_id)
        except Dataset.DoesNotExist:
            return Response({"detail": "Dataset not found."}, status=status.HTTP_404_NOT_FOUND)

        table_name = dataset.table_name

        # Build the SQL query with optional filters
        query = f'SELECT * FROM "{table_name}"'
        conditions = []
        if start_ms:
            conditions.append(f"timestamp >= {start_ms}")
        if end_ms:
            conditions.append(f"timestamp <= {end_ms}")
        if conditions:
            query += " WHERE " + " AND ".join(conditions)

        # Execute the query
        with connection.cursor() as cursor:
            cursor.execute(query)
            columns = [col[0] for col in cursor.description]
            rows = [dict(zip(columns, row)) for row in cursor.fetchall()]

        return Response(rows, status=status.HTTP_200_OK)

    def post(self, request, dataset_id):
        """
        Insert multiple rows into the dataset's table.
        """
        # Get the dataset and its table name
        try:
            dataset = Dataset.objects.get(id=dataset_id)
        except Dataset.DoesNotExist:
            return Response({"detail": "Dataset not found."}, status=status.HTTP_404_NOT_FOUND)

        table_name = dataset.table_name
        data_points = request.data

        if not isinstance(data_points, list):
            return Response(
                {"detail": "Expected a list of data points."},
                status=status.HTTP_400_BAD_REQUEST
            )

        # Validate if columns exist in dataset columns
        dataset_columns = DatasetColumn.objects.filter(dataset_type=dataset.dataset_type)
        valid_columns = {col.mnemonic for col in dataset_columns}
        valid_columns.add('timestamp')

        # Build the SQL query for insertion
        rows = []
        for data in data_points:
            invalid_columns = [col for col in data.keys() if col not in valid_columns]
            if invalid_columns:
                return Response(
                    {"detail": f"Invalid columns: {', '.join(invalid_columns)}"},
                    status=status.HTTP_400_BAD_REQUEST
                )
            columns = ', '.join(data.keys())
            values = ', '.join([f"'{value}'" for value in data.values()])
            rows.append(f"({values})")

        if not rows:
            return Response(
                {"detail": "No valid data points provided."},
                status=status.HTTP_400_BAD_REQUEST
            )

        query = f'INSERT INTO "{table_name}" ({columns}) VALUES {", ".join(rows)}'

        # Execute the query
        with connection.cursor() as cursor:
            cursor.execute(query)

        return Response({"detail": "Rows inserted successfully."}, status=status.HTTP_201_CREATED)

    def delete(self, request, dataset_id):
        """
        Delete rows from the dataset's table with optional filtering by start_ms and end_ms.
        """
        start_ms = request.query_params.get('start_ms')
        end_ms = request.query_params.get('end_ms')

        # Get the dataset and its table name
        try:
            dataset = Dataset.objects.get(id=dataset_id)
        except Dataset.DoesNotExist:
            return Response({"detail": "Dataset not found."}, status=status.HTTP_404_NOT_FOUND)

        table_name = dataset.table_name

        # Build the SQL query for deletion
        query = f'DELETE FROM "{table_name}"'
        conditions = []
        if start_ms:
            conditions.append(f"start_ms >= {start_ms}")
        if end_ms:
            conditions.append(f"end_ms <= {end_ms}")
        if conditions:
            query += " WHERE " + " AND ".join(conditions)

        # Execute the query
        with connection.cursor() as cursor:
            cursor.execute(query)

        return Response({"detail": "Rows deleted successfully."}, status=status.HTTP_200_OK)