# Generated by Django 5.0.2 on 2024-02-13 17:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('currency_converter', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='conversionhistory',
            name='currency',
            field=models.CharField(max_length=6),
        ),
    ]
