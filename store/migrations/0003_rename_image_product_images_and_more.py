# Generated by Django 5.0.6 on 2024-06-04 13:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0002_reviewrating'),
    ]

    operations = [
        migrations.RenameField(
            model_name='product',
            old_name='image',
            new_name='images',
        ),
        migrations.AlterField(
            model_name='product',
            name='description',
            field=models.TextField(max_length=500, unique=True),
        ),
        migrations.AlterField(
            model_name='product',
            name='product_name',
            field=models.CharField(max_length=200, unique=True),
        ),
    ]
