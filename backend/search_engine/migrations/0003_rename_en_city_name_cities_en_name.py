# Generated by Django 4.2.5 on 2023-11-15 16:17

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('search_engine', '0002_rename_city_code_cities_code_and_more'),
    ]

    operations = [
        migrations.RenameField(
            model_name='cities',
            old_name='en_city_name',
            new_name='en_name',
        ),
    ]
