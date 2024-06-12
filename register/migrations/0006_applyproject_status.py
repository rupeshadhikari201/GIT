# Generated by Django 5.0.2 on 2024-06-12 13:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("register", "0005_notification"),
    ]

    operations = [
        migrations.AddField(
            model_name="applyproject",
            name="status",
            field=models.CharField(
                choices=[
                    ("PA", "Pending Approval"),
                    ("AC", "Accepted"),
                    ("RE", "Rejected"),
                ],
                default="PA",
                max_length=2,
            ),
        ),
    ]
