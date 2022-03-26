# Generated by Django 4.0 on 2022-03-26 15:29

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0015_alter_gameteam_unique_together_gameteamstat'),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='game',
            unique_together={('day', 'gid')},
        ),
        migrations.AlterUniqueTogether(
            name='seasonday',
            unique_together={('season', 'day_num')},
        ),
        migrations.AlterUniqueTogether(
            name='teamcoach',
            unique_together={('team', 'coach', 'first_day')},
        ),
        migrations.AlterUniqueTogether(
            name='teamconference',
            unique_together={('team', 'season')},
        ),
        migrations.AlterUniqueTogether(
            name='teamrank',
            unique_together={('team', 'season', 'ranking_day', 'system')},
        ),
    ]
