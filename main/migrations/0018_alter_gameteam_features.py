# Generated by Django 4.0 on 2022-03-27 12:41

import django.contrib.postgres.fields.hstore
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0017_gameteam_features'),
    ]

    operations = [
        migrations.AlterField(
            model_name='gameteam',
            name='features',
            field=django.contrib.postgres.fields.hstore.HStoreField(default=dict, null=True),
        ),
    ]
