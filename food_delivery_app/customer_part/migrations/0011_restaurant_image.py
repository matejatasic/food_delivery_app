# Generated by Django 4.2.7 on 2023-12-27 12:39

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("customer_part", "0010_rename_restaurantlikes_restaurantlike_and_more"),
    ]

    operations = [
        migrations.AddField(
            model_name="restaurant",
            name="image",
            field=models.ImageField(upload_to="restaurant_pictures"),
        ),
    ]
