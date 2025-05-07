from typing import Optional
from django.db import models
import uuid

class Well(models.Model):
    id: models.UUIDField = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False) # type: ignore
    name: models.CharField = models.CharField(max_length=255) # type: ignore
    location: models.CharField = models.CharField(max_length=255, blank=True, null=True) # type: ignore
    created_at: models.DateTimeField = models.DateTimeField(auto_now_add=True) # type: ignore

    def __str__(self) -> str:
        return self.name # type: ignore
    





