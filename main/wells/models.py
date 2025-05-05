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
    

class DatasetType(models.Model):
    name = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.name

class DatasetColumn(models.Model):
    dataset_type = models.ForeignKey(DatasetType, on_delete=models.CASCADE, related_name="columns")
    mnemonic = models.CharField(max_length=100, unique=True)
    name = models.CharField(max_length=100)
    uom = models.CharField(max_length=50)
    data_type = models.CharField(max_length=20, choices=[("float", "Float"), ("int", "Integer"), ("text", "Text")])

    def __str__(self):
        return f"{self.mnemonic} | {self.name} ({self.uom})"
    

class Dataset(models.Model):
    dataset_type = models.ForeignKey(DatasetType, on_delete=models.CASCADE, related_name="datasets")
    well = models.ForeignKey(Well, on_delete=models.CASCADE, related_name="datasets")
    table_name = models.CharField(max_length=128, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = [("dataset_type", "well")]

    def __str__(self):
        return f"{self.dataset_type.name} for {self.well.name}"




