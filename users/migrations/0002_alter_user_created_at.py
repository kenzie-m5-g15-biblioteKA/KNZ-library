# Generated by Django 4.2.2 on 2023-07-11 20:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("users", "0001_initial"),
    ]

    operations = [
        migrations.AlterField(
            model_name="user",
            name="created_at",
            field=models.DateField(auto_now_add=True),
        ),
    ]