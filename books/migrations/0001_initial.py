# Generated by Django 4.2.2 on 2023-07-07 20:36

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="Book",
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
                ("title", models.CharField(max_length=255)),
                ("author", models.CharField(max_length=100)),
                ("published_date", models.DateField()),
                ("publishing_company", models.CharField(max_length=100)),
                (
                    "availability",
                    models.CharField(
                        choices=[
                            ("unavailable", "Unavailable"),
                            ("available", "Available"),
                        ],
                        default="available",
                        max_length=255,
                    ),
                ),
            ],
            options={
                "ordering": ["id"],
            },
        ),
    ]
