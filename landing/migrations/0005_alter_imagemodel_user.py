# Generated by Django 4.2.2 on 2023-07-02 17:24

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    dependencies = [
        ("landing", "0004_alter_imagemodel_user"),
    ]

    operations = [
        migrations.AlterField(
            model_name="imagemodel",
            name="user",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL
            ),
        ),
    ]
