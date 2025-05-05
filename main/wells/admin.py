from django.contrib import admin
from .models import Well
from .models import Dataset

@admin.register(Well)
class WellAdmin(admin.ModelAdmin): # type: ignore
    list_display = ('id', 'name', 'location', 'created_at')
    search_fields = ('name',)

@admin.register(Dataset)
class DatasetAdmin(admin.ModelAdmin):
    list_display = ('dataset_type_id', 'well_id', 'table_name', 'created_at')
    list_filter = ('dataset_type_id', 'well_id')
    search_fields = ('table_name', 'well__name')
    ordering = ('-created_at',)
