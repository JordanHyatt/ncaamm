# Generated by Django 4.0 on 2022-03-26 10:16

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='City',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('kid', models.IntegerField(unique=True, verbose_name="Kaggle's Unique ID")),
                ('name', models.CharField(max_length=200)),
                ('state', models.CharField(max_length=2)),
            ],
        ),
    ]