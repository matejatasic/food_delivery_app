# Generated by Django 4.2.7 on 2023-12-27 15:29

from django.db import migrations


class Migration(migrations.Migration):
    dependencies = [
        ("customer_part", "0011_restaurant_image"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="restaurantlike",
            name="is_dislike",
        ),
    ]
