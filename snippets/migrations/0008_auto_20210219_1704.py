# Generated by Django 3.0.7 on 2021-02-19 22:04

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('snippets', '0007_auto_20210219_1702'),
    ]

    operations = [
        migrations.DeleteModel(
            name='Pizza',
        ),
        migrations.DeleteModel(
            name='Topping',
        ),
    ]
