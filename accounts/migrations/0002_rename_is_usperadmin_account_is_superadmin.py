# Generated by Django 5.0.6 on 2024-06-04 07:23

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='account',
            old_name='is_usperadmin',
            new_name='is_superadmin',
        ),
    ]
