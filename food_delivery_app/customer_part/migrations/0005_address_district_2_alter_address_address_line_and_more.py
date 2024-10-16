# Generated by Django 4.2.7 on 2023-12-14 07:50

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("customer_part", "0004_address"),
    ]

    operations = [
        migrations.AddField(
            model_name="address",
            name="district_2",
            field=models.CharField(),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name="address",
            name="address_line",
            field=models.CharField(max_length=50, null=True),
        ),
        migrations.AlterField(
            model_name="address",
            name="postal_code",
            field=models.IntegerField(null=True),
        ),
    ]
