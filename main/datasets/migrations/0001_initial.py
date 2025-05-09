# Generated by Django 5.2 on 2025-05-07 12:11

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ("wells", "0001_initial"),
    ]

    operations = [
        migrations.CreateModel(
            name="DatasetType",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("name", models.CharField(max_length=100, unique=True)),
            ],
        ),
        migrations.CreateModel(
            name="DatasetColumn",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("mnemonic", models.CharField(max_length=100, unique=True)),
                ("name", models.CharField(max_length=100)),
                ("uom", models.CharField(max_length=50)),
                (
                    "data_type",
                    models.CharField(
                        choices=[
                            ("float", "Float"),
                            ("int", "Integer"),
                            ("text", "Text"),
                        ],
                        max_length=20,
                    ),
                ),
                (
                    "dataset_type",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="columns",
                        to="datasets.datasettype",
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="Dataset",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("table_name", models.CharField(max_length=128, unique=True)),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                (
                    "well",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="datasets",
                        to="wells.well",
                    ),
                ),
                (
                    "dataset_type",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="datasets",
                        to="datasets.datasettype",
                    ),
                ),
            ],
            options={
                "unique_together": {("dataset_type", "well")},
            },
        ),
    ]
