# Generated by Django 4.2.2 on 2023-07-10 19:17

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ("books", "0001_initial"),
        ("assessments", "0001_initial"),
    ]

    operations = [
        migrations.AddField(
            model_name="assessments",
            name="book",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE,
                related_name="assessments",
                to="books.book",
            ),
        ),
    ]
