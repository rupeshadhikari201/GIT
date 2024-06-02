# Generated by Django 5.0.2 on 2024-06-02 13:02

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("register", "0001_initial"),
    ]

    operations = [
        migrations.CreateModel(
            name="ApplyProject",
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
                ("applied_at", models.DateTimeField(auto_now_add=True)),
                ("proposal", models.TextField()),
                (
                    "frelancer_id",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="register.freelancer",
                    ),
                ),
                (
                    "project_id",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="register.projects",
                    ),
                ),
            ],
        ),
    ]
