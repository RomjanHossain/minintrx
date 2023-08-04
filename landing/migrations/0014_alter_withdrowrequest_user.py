# Generated by Django 4.2.2 on 2023-07-28 06:25

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    dependencies = [
        ("landing", "0013_alter_withdrowrequest_user"),
    ]

    operations = [
        migrations.AlterField(
            model_name="withdrowrequest",
            name="user",
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.CASCADE,
                to=settings.AUTH_USER_MODEL,
            ),
        ),
    ]
