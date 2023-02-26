# Generated by Django 3.2.15 on 2022-11-05 15:59

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    dependencies = [
        ("members", "0031_auto_20221101_1034"),
    ]

    operations = [
        migrations.AlterField(
            model_name="activity",
            name="union",
            field=models.ForeignKey(
                default=1,
                on_delete=django.db.models.deletion.CASCADE,
                to="members.union",
                verbose_name="Forening",
            ),
        ),
    ]
