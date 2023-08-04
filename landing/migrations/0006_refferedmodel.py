# Generated by Django 4.2.2 on 2023-07-17 23:40

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    dependencies = [
        ("landing", "0005_alter_imagemodel_user"),
    ]

    operations = [
        migrations.CreateModel(
            name="RefferedModel",
            fields=[
                ("id", models.AutoField(primary_key=True, serialize=False)),
                ("reffer_code", models.CharField(max_length=1000)),
                ("amount", models.FloatField(default=0.0)),
                ("date", models.DateTimeField(auto_now_add=True)),
                (
                    "reffered_user",
                    models.ManyToManyField(
                        related_name="reffered_user", to=settings.AUTH_USER_MODEL
                    ),
                ),
                (
                    "user",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
            ],
            options={
                "verbose_name_plural": "Reffered Code",
            },
        ),
    ]