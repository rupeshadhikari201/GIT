# Generated by Django 5.0.2 on 2024-03-08 06:59

import django.contrib.postgres.fields
import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("register", "0002_alter_user_user_type"),
    ]

    operations = [
        migrations.CreateModel(
            name="Freelancer",
            fields=[
                (
                    "user",
                    models.OneToOneField(
                        on_delete=django.db.models.deletion.CASCADE,
                        primary_key=True,
                        serialize=False,
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
                ("profession", models.CharField(max_length=255)),
                (
                    "skills",
                    django.contrib.postgres.fields.ArrayField(
                        base_field=models.CharField(max_length=100),
                        blank=True,
                        null=True,
                        size=None,
                    ),
                ),
                (
                    "languages",
                    django.contrib.postgres.fields.ArrayField(
                        base_field=models.CharField(max_length=100),
                        blank=True,
                        null=True,
                        size=None,
                    ),
                ),
                ("reason_to_join", models.TextField()),
                (
                    "where_did_you_heard",
                    models.CharField(
                        choices=[
                            ("I", "Instagram"),
                            ("F", "Facebook"),
                            ("T", "Twitter"),
                            ("G", "Google"),
                            ("O", "Others"),
                        ],
                        max_length=1,
                    ),
                ),
                (
                    "resume",
                    models.FileField(blank=True, null=True, upload_to="resumes/"),
                ),
                ("bio", models.TextField()),
            ],
        ),
        migrations.CreateModel(
            name="Payment",
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
                ("amount", models.DecimalField(decimal_places=2, max_digits=10)),
            ],
        ),
        migrations.CreateModel(
            name="PaymentStatus",
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
                (
                    "payment_status",
                    models.CharField(
                        choices=[
                            ("P", "Paid"),
                            ("UN", "Unpaid"),
                            ("PP", "Partially Paid"),
                        ]
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="ProjectStatus",
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
                (
                    "project_status",
                    models.CharField(
                        choices=[("C", "Completed"), ("O", "Onging"), ("P", "Paused")]
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="Client",
            fields=[
                (
                    "user",
                    models.OneToOneField(
                        on_delete=django.db.models.deletion.CASCADE,
                        primary_key=True,
                        serialize=False,
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
                (
                    "payments_paid",
                    models.ManyToManyField(
                        related_name="payments_paid_by_clients", to="register.payment"
                    ),
                ),
            ],
        ),
        migrations.AddField(
            model_name="payment",
            name="payment_status",
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.SET_NULL,
                to="register.paymentstatus",
            ),
        ),
        migrations.CreateModel(
            name="Projects",
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
                (
                    "project_category",
                    models.CharField(
                        choices=[
                            ("R", "Research"),
                            ("D", "Design"),
                            ("Dev", "Development"),
                        ]
                    ),
                ),
                ("title", models.CharField(max_length=255)),
                ("description", models.TextField()),
                ("project_price", models.IntegerField()),
                ("project_deadline", models.DateTimeField()),
                (
                    "skills_required",
                    django.contrib.postgres.fields.ArrayField(
                        base_field=models.CharField(max_length=100),
                        blank=True,
                        null=True,
                        size=None,
                    ),
                ),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("updated_at", models.DateTimeField()),
                (
                    "client",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="projects_created",
                        to="register.client",
                    ),
                ),
                (
                    "freelancer",
                    models.ForeignKey(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.SET_NULL,
                        related_name="projects_allocated",
                        to="register.freelancer",
                    ),
                ),
                (
                    "payment_status",
                    models.ForeignKey(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.SET_NULL,
                        to="register.paymentstatus",
                    ),
                ),
                (
                    "project_status",
                    models.ForeignKey(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.SET_NULL,
                        to="register.projectstatus",
                    ),
                ),
            ],
        ),
        migrations.AddField(
            model_name="payment",
            name="project",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE,
                related_name="payments",
                to="register.projects",
            ),
        ),
        migrations.AddField(
            model_name="client",
            name="projects_uploaded",
            field=models.ManyToManyField(
                related_name="uploaded_by_clients", to="register.projects"
            ),
        ),
    ]
