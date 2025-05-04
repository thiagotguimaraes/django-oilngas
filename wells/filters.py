from django_filters import rest_framework as filters
from .models import Well

class WellFullFilter(filters.FilterSet):
    start_ms = filters.NumberFilter(method='filter_by_time_range')
    end_ms = filters.NumberFilter(method='filter_by_time_range')
    name = filters.CharFilter(field_name='name', lookup_expr='icontains')
    location = filters.CharFilter(field_name='location', lookup_expr='icontains')


    def filter_by_time_range(self, queryset, name, value):
        start = self.data.get('start_ms')
        end = self.data.get('end_ms')

        # Convert to integers
        start = int(start) if start is not None else None
        end = int(end) if end is not None else None

        if start is not None and end is not None:
            # boundaries must overlap the range
            return queryset.filter(boundaries__start_ms__lte=end, boundaries__end_ms__gte=start)
        elif start is not None:
            # boundary ends after start
            return queryset.filter(boundaries__end_ms__gte=start)
        elif end is not None:
            # boundary starts before end
            return queryset.filter(boundaries__start_ms__lte=end)

        return queryset  # No filtering if neither is passed

    class Meta:
        model = Well
        fields = ['name', 'location']
