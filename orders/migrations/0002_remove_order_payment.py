# Generated by Django 5.0.6 on 2024-06-02 17:53

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('orders', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='order',
            name='payment',
        ),
    ]