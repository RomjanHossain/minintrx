# Generated by Django 4.2.2 on 2023-07-02 17:24

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("landing", "0003_rename_package_packagemodel_quiz_point_and_more"),
    ]

    operations = [
        migrations.AlterField(
            model_name="imagemodel",
            name="user",
            field=models.CharField(max_length=50),
        ),
    ]
