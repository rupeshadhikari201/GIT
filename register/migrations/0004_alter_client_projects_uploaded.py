# Generated by Django 5.0.2 on 2024-03-08 09:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("register", "0003_freelancer_payment_paymentstatus_projectstatus_and_more"),
    ]

    operations = [
        migrations.AlterField(
            model_name="client",
            name="projects_uploaded",
            field=models.ManyToManyField(
                null=True, related_name="uploaded_by_clients", to="register.projects"
            ),
        ),
    ]
