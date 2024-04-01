# Generated by Django 5.0.2 on 2024-03-08 11:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("register", "0005_alter_projects_updated_at"),
    ]

    operations = [
        migrations.RemoveField(model_name="client", name="payments_paid",),
        migrations.AlterField(
            model_name="client",
            name="projects_uploaded",
            field=models.ManyToManyField(
                related_name="uploaded_by_clients", to="register.projects"
            ),
        ),
    ]
