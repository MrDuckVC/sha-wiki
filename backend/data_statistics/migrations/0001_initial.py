# Generated by Django 4.2.5 on 2024-04-17 18:43

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Statistics',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('type', models.CharField(choices=[('corporation_count', 'Corporation count'), ('prefecture_count', 'Prefecture count'), ('last_update', 'Last update'), ('last_updated_corporations_count', 'Last updated corporations count'), ('youngest_corporations', 'Youngest corporations'), ('oldest_corporations', 'Oldest corporations'), ('longest_name_corporations', 'Longest name corporations'), ('foreign_corporations', 'Foreign corporations')], max_length=50, unique=True)),
                ('value', models.JSONField()),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
            ],
            options={
                'verbose_name_plural': 'statistics',
                'db_table': 'statistics',
            },
        ),
    ]
