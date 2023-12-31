# Generated by Django 4.2.7 on 2023-11-25 05:01

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("taxi_project", "0001_initial"),
    ]

    operations = [
        migrations.CreateModel(
            name="CartItem",
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
                ("product", models.CharField(max_length=100)),
                ("purchased", models.BooleanField(default=False)),
            ],
        ),
        migrations.RemoveField(
            model_name="tripdetails",
            name="customer",
        ),
    ]
