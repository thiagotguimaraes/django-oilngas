from rest_framework import serializers
from main.datasets.serializers import DatasetSerializer
from main.wells.models import Well

class WellSerializer(serializers.ModelSerializer):
    class Meta:
        model = Well
        fields = '__all__'

class WellFullSerializer(serializers.ModelSerializer):
    datasets = DatasetSerializer(many=True, read_only=True)

    class Meta:
        model = Well
        fields = ['id', 'name', 'location', 'created_at', 'datasets']
