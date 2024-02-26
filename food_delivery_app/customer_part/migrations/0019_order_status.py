# Generated by Django 4.2.7 on 2024-02-08 16:37

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("customer_part", "0018_order_orderitem"),
    ]

    operations = [
        migrations.AddField(
            model_name="order",
            name="status",
            field=models.CharField(
                choices=[
                    ("Ordered", "Ordered"),
                    ("Being Transported", "Being Transported"),
                    ("Delivered", "Delivered"),
                ],
                default="Ordered",
            ),
        ),
    ]
