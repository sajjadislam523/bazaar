# Generated by Django 5.0.6 on 2024-06-04 07:23

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0002_rename_is_usperadmin_account_is_superadmin'),
        ('cart', '0004_alter_cartitem_product'),
    ]

    operations = [
        migrations.AlterField(
            model_name='cart',
            name='date_added',
            field=models.DateField(auto_now_add=True),
        ),
        migrations.AlterField(
            model_name='cartitem',
            name='user',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='accounts.account'),
        ),
    ]