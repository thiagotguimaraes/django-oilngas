from typing import Optional
from django.db import models
import uuid

class Well(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=255)
    location = models.CharField(max_length=255, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name
    

class WellBoundaries(models.Model):
    well = models.OneToOneField("Well", on_delete=models.CASCADE, primary_key=True, related_name="boundaries")
    start_ms: Optional[int] = models.BigIntegerField(null=True, blank=True)
    end_ms: Optional[int] = models.BigIntegerField(null=True, blank=True)

    def __str__(self):
        return f"Boundaries for {self.well.name}"

