# Generated by Django 4.0 on 2022-03-26 10:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0002_confernce'),
    ]

    operations = [
        migrations.AlterField(
            model_name='confernce',
            name='abbrv',
            field=models.CharField(max_length=100, unique=True),
        ),
    ]