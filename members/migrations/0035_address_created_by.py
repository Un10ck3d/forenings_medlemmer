# Generated by Django 4.1.3 on 2022-12-29 13:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("members", "0034_address_created_at"),
    ]

    operations = [
        migrations.AddField(
            model_name="address",
            name="created_by",
            field=models.PositiveIntegerField(default=0, verbose_name="Oprettet af"),
        ),
    ]
