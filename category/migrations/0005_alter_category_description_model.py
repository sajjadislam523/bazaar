# Generated by Django 5.0.6 on 2024-06-04 11:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('category', '0004_rename_description_category_description_model'),
    ]

    operations = [
        migrations.AlterField(
            model_name='category',
            name='description_model',
            field=models.TextField(blank=True, max_length=500),
        ),
    ]
