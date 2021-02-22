# Generated by Django 3.0.7 on 2021-02-19 20:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('snippets', '0005_author_book'),
    ]

    operations = [
        migrations.CreateModel(
            name='Topping',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50)),
            ],
        ),
        migrations.CreateModel(
            name='Pizza',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50)),
                ('toppings', models.ManyToManyField(to='snippets.Topping')),
            ],
        ),
    ]
