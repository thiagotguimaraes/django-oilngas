from django.contrib import admin
from main.wells.models import Well

@admin.register(Well)
class WellAdmin(admin.ModelAdmin): # type: ignore
    list_display = ('id', 'name', 'location', 'created_at')
    search_fields = ('name',)

