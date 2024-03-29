# Generated by Django 4.0 on 2022-03-26 11:42

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0009_teamrank'),
    ]

    operations = [
        migrations.CreateModel(
            name='Game',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('num_ot', models.IntegerField()),
                ('city', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='main.city')),
                ('day', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='main.seasonday')),
                ('season', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='main.season')),
                ('teams', models.ManyToManyField(to='main.Team')),
            ],
        ),
        migrations.CreateModel(
            name='GameTeam',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('loc', models.CharField(choices=[('H', 'Home'), ('A', 'Away'), ('N', 'Neutral')], max_length=10)),
                ('result', models.CharField(choices=[('win', 'Win'), ('loss', 'Loss')], max_length=10)),
                ('game', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='main.game')),
                ('opponent', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='gameteam_opp_set', to='main.team')),
                ('team', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='gameteam_set', to='main.team')),
            ],
        ),
    ]
