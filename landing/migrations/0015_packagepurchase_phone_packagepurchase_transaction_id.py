# Generated by Django 4.2.2 on 2023-07-28 10:07

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("landing", "0014_alter_withdrowrequest_user"),
    ]

    operations = [
        migrations.AddField(
            model_name="packagepurchase",
            name="phone",
            field=models.CharField(default=None, max_length=1000),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name="packagepurchase",
            name="transaction_id",
            field=models.CharField(default=None, max_length=1000),
            preserve_default=False,
        ),
    ]
