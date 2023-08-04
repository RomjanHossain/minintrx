# Generated by Django 4.2.2 on 2023-07-02 17:23

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    dependencies = [
        ("landing", "0002_package_quiz_scratchcard_spin_visitwebsites_and_more"),
    ]

    operations = [
        migrations.RenameModel(
            old_name="Package",
            new_name="PackageModel",
        ),
        migrations.AddField(
            model_name="quiz",
            name="point",
            field=models.FloatField(default=0.0),
        ),
        migrations.AlterField(
            model_name="imagemodel",
            name="user",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL
            ),
        ),
    ]
