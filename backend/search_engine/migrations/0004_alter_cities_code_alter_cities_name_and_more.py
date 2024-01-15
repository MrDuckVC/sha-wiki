# Generated by Django 4.2.5 on 2023-11-26 08:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('search_engine', '0003_rename_en_city_name_cities_en_name'),
    ]

    operations = [
        migrations.AlterField(
            model_name='cities',
            name='code',
            field=models.SmallIntegerField(),
        ),
        migrations.AlterField(
            model_name='cities',
            name='name',
            field=models.CharField(max_length=128),
        ),
        migrations.AlterField(
            model_name='prefectures',
            name='code',
            field=models.CharField(max_length=2, unique=True),
        ),
        migrations.AlterField(
            model_name='prefectures',
            name='en_name',
            field=models.CharField(max_length=128),
        ),
        migrations.AlterField(
            model_name='prefectures',
            name='name',
            field=models.CharField(max_length=128),
        ),
    ]