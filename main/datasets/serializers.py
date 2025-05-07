from rest_framework import serializers
import re
from main.datasets.models import Dataset
from main.datasets.models import DatasetType, DatasetColumn
from main.wells.models import Well

class DatasetColumnSerializer(serializers.ModelSerializer):
    dataset_type_id = serializers.PrimaryKeyRelatedField(
        source='dataset_type', queryset=DatasetType.objects.all()
    )

    class Meta:
        model = DatasetColumn
        fields = ['id', 'dataset_type_id', 'name', 'mnemonic', 'uom', 'data_type']

    def validate_mnemonic(self, value):
        if not re.match(r'^[a-z_][a-z0-9_]*$', value):
            raise serializers.ValidationError(
                "Mnemonic must be lowercase, start with a letter or underscore, and contain only lowercase letters, numbers, or underscores."
            )
        return value

class DatasetTypeSerializer(serializers.ModelSerializer):
    columns = DatasetColumnSerializer(many=True, read_only=True)

    class Meta:
        model = DatasetType
        fields = ['id', 'name', 'columns']

    def validate_name(self, value):
        if not re.match(r'^[a-z_][a-z0-9_]*$', value):
            raise serializers.ValidationError(
                "Name must be lowercase, start with a letter or underscore, and contain only lowercase letters, numbers, or underscores."
            )
        return value

class DatasetSerializer(serializers.ModelSerializer):
    dataset_type = DatasetTypeSerializer(read_only=True)

    dataset_type_id = serializers.PrimaryKeyRelatedField(
        source='dataset_type', queryset=DatasetType.objects.all()
    )
    well_id = serializers.PrimaryKeyRelatedField(
        source='well', queryset=Well.objects.all()
    )
    
    class Meta:
        model = Dataset
        fields = ['id', 'dataset_type_id', 'well_id', 'table_name', 'dataset_type', 'created_at']
        read_only_fields = ['dataset_type_id', 'well_id', 'table_name', 'dataset_type', 'created_at']
