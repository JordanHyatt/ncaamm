# Generated by Django 4.0 on 2022-03-26 10:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Confernce',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('abbrv', models.CharField(max_length=2, unique=True)),
                ('name', models.CharField(max_length=200)),
            ],
        ),
    ]