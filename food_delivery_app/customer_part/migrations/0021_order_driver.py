# Generated by Django 4.2.7 on 2024-02-22 15:56

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ("customer_part", "0020_alter_orderitem_item"),
    ]

    operations = [
        migrations.AddField(
            model_name="order",
            name="driver",
            field=models.ForeignKey(
                default=None,
                null=True,
                on_delete=django.db.models.deletion.SET_NULL,
                related_name="driver",
                to=settings.AUTH_USER_MODEL,
            ),
        ),
    ]
