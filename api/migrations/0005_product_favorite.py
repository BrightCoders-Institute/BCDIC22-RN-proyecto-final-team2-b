# Generated by Django 4.1.7 on 2023-03-14 23:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0004_rename_product_id_reviews_product_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='favorite',
            field=models.BooleanField(blank=True, default=False, null=True),
        ),
    ]
