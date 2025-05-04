from rest_framework import serializers
from .models import Well
from .models import WellBoundaries


class WellSerializer(serializers.ModelSerializer):
    class Meta:
        model = Well
        fields = '__all__'

class WellBoundariesSerializer(serializers.ModelSerializer):
    class Meta:
        model = WellBoundaries
        fields = '__all__'

class WellFullSerializer(serializers.ModelSerializer):
    boundaries = WellBoundariesSerializer(read_only=True)

    class Meta:
        model = Well
        fields = ['id', 'name', 'location', 'created_at', 'boundaries']