# Generated by Django 4.0 on 2022-04-14 15:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0019_tourneyseed_zeropad'),
    ]

    operations = [
        migrations.AlterField(
            model_name='zeropad',
            name='num',
            field=models.IntegerField(unique=True),
        ),
    ]