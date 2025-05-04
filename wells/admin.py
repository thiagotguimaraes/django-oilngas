from django.contrib import admin
from .models import Well
from .models import WellBoundaries


@admin.register(Well)
class WellAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'location', 'created_at')
    search_fields = ('name',)


@admin.register(WellBoundaries)
class WellBoundariesAdmin(admin.ModelAdmin):
    list_display = ('well', 'start_ms', 'end_ms')
    search_fields = ('well__name',)