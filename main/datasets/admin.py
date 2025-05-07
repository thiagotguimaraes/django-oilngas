from django.contrib import admin
from main.datasets.models import Dataset

@admin.register(Dataset)
class DatasetAdmin(admin.ModelAdmin):
    list_display = ('dataset_type_id', 'well_id', 'table_name', 'created_at')
    list_filter = ('dataset_type_id', 'well_id')
    search_fields = ('table_name', 'well__name')
    ordering = ('-created_at',)
