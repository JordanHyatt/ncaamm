from django.db import models
from django.conf import settings
import pandas as pd
from tqdm import tqdm
import os

class City(models.Model):
    ''' Represents a city a game could be played in '''
    kid = models.IntegerField(verbose_name="Kaggle's Unique ID", unique=True)
    name = models.CharField(max_length=200)
    state = models.CharField(max_length=2)

    @classmethod
    def update_objs(cls):
        ''' A method to update cities from csv '''
        path = os.path.join(settings.BASE_DATA_PATH, 'Cities.csv')
        df = pd.read_csv(path)
        for tup in tqdm(df.itertuples()):
            obj, _ = cls.objects.update_or_create(
                kid=tup.CityID,
                defaults=dict(
                    name=tup.City, state=tup.State
                )
            )

    def __str__(self):
        return f'{self.name} | {self.state}'


class Conference(models.Model):
    ''' Represents a Mens NCAA Basketball conference '''
    abbrv = models.CharField(max_length=100, unique=True)
    name = models.CharField(max_length=200)
    

    @classmethod
    def update_objs(cls):
        ''' A method to update conferences from csv '''
        path = os.path.join(settings.BASE_DATA_PATH, 'Conferences.csv')
        df = pd.read_csv(path)
        for tup in tqdm(df.itertuples()):
            obj, _ = cls.objects.update_or_create(
                abbrv = tup.ConfAbbrev,
                defaults=dict(
                    name=tup.Description
                )
            )

    def __str__(self):
        return f'{self.name}'


class Season(models.Model):
    ''' Represents a Mens NCAA Basketball Season '''
    year = models.IntegerField(verbose_name='Year Season Ended',unique=True)
    sdate = models.DateField(verbose_name='Season Start Date', null=True)

    @classmethod
    def update_objs(cls):
        ''' A method to update seasons from csv '''
        path = os.path.join(settings.BASE_DATA_PATH, 'MSeasons.csv')
        df = pd.read_csv(path)
        for tup in tqdm(df.itertuples()):
            obj, _ = cls.objects.update_or_create(
                year=tup.Season,
                defaults=dict(
                    sdate = pd.to_datetime(tup.DayZero)
                )
            )

    def __str__(self):
        return f'{self.year}'


class Team(models.Model):
    ''' Represents a Mens NCAA Basketball Team '''
    kid = models.IntegerField(verbose_name="Kaggle's Unique ID", unique=True)
    name = models.CharField(max_length=200) 
    
    @classmethod
    def update_objs(cls):
        ''' A method to update conferences from csv '''
        path = os.path.join(settings.BASE_DATA_PATH, 'MTeams.csv')
        df = pd.read_csv(path)
        for tup in tqdm(df.itertuples()):
            obj, _ = cls.objects.update_or_create(
                kid=tup.TeamID,
                defaults=dict(
                    name=tup.TeamName
                )
            )

    def __str__(self):
        return f'{self.name}'

class SeasonDay(models.Model):
    ''' Represents a day during a season '''
    season = models.ForeignKey('Season', on_delete=models.CASCADE)
    day_num = models.IntegerField()

    class Meta:
        unique_together = ['season', 'day_num']

    def __str__(self):
        return f'{self.season} | {self.day_num}'

class Coach(models.Model):
    ''' Represents a Mens NCAA Baseketball coach '''
    kname = models.CharField(max_length=200, unique=True)

    def __str__(self):
        return f'{self.kname}'

class TeamCoach(models.Model):
    ''' Represents a instance of a coach coaching a team during a season '''
    team = models.ForeignKey('Team', on_delete=models.CASCADE)
    coach = models.ForeignKey('Coach', on_delete=models.CASCADE)
    season = models.ForeignKey('Season', on_delete=models.CASCADE)
    first_day = models.ForeignKey('SeasonDay', on_delete=models.CASCADE, related_name='first_day_set')
    last_day = models.ForeignKey('SeasonDay', on_delete=models.CASCADE, related_name='last_day_set')

    class Meta:
        unique_together = ['team', 'coach', 'first_day']

    @classmethod
    def update_objs(cls):
        ''' A method to update conferences from csv '''
        path = os.path.join(settings.BASE_DATA_PATH, 'MTeamCoaches.csv')
        df = pd.read_csv(path)
        for tup in tqdm(df.itertuples()):
            coach,_ = Coach.objects.get_or_create(kname=tup.CoachName)
            season = Season.objects.filter(year=tup.Season).first()
            team = Team.objects.filter(kid=tup.TeamID).first()
            fd,_ = SeasonDay.objects.get_or_create(
                season=season, day_num=tup.FirstDayNum
            )
            ld,_ = SeasonDay.objects.get_or_create(
                season=season, day_num=tup.LastDayNum
            )
            obj, _ = cls.objects.update_or_create(
                team=team, coach=coach, first_day=fd, last_day=ld,
                defaults=dict(season=season)
            )

    def __str__(self):
        return f'{self.coach} | {self.season} | {self.team} | {self.first_day.num} -> {self.last_day.num}'


class TeamConference(models.Model):
    ''' Represents which conference a team was in for a given season '''
    team = models.ForeignKey('Team', on_delete=models.CASCADE)
    season = models.ForeignKey('Season', on_delete=models.CASCADE)
    conference = models.ForeignKey('Conference', on_delete=models.CASCADE)

    class Meta:
        unique_together = ['team', 'season']

    @classmethod
    def update_objs(cls):
        ''' A method to update conferences from csv '''
        path = os.path.join(settings.BASE_DATA_PATH, 'MTeamConferences.csv')
        df = pd.read_csv(path)
        for tup in tqdm(df.itertuples()):
            conf = Conference.objects.filter(abbrv=tup.ConfAbbrev).first()
            season = Season.objects.filter(year=tup.Season).first()
            team = Team.objects.filter(kid=tup.TeamID).first()
            obj, _ = cls.objects.update_or_create(
                team=team, conference=conf, season=season
            )

    def __str__(self):
        return f'{self.season} | {self.team} | {self.conference}'


class TeamRank(models.Model):
    ''' Represents a Mens NCAA Basketball team ranking by a given system on a given season day '''
    team = models.ForeignKey('Team', on_delete=models.CASCADE)
    season = models.ForeignKey('Season', on_delete=models.CASCADE)
    ranking_day = models.ForeignKey('SeasonDay', on_delete=models.CASCADE)
    system = models.CharField(max_length=20)
    rank = models.IntegerField()

    class Meta:
        unique_together = ['team', 'season', 'ranking_day', 'system']

    @classmethod
    def update_objs(cls):
        ''' A method to update team rankings from csv '''
        path = os.path.join(settings.BASE_DATA_PATH, 'MMasseyOrdinals_thruDay128.csv')
        df = pd.read_csv(path)
        for tup in tqdm(df.itertuples()):
            season = Season.objects.filter(year=tup.Season).first()
            team = Team.objects.filter(kid=tup.TeamID).first()
            rd,_ = SeasonDay.objects.get_or_create(season=season, day_num=tup.RankingDayNum)
            obj, _ = cls.objects.update_or_create(
                team=team, ranking_day=rd, system=tup.SystemName,
                defaults=dict(season=season, rank=tup.OrdinalRank)
            )

    def __str__(self):
        return f'{self.ranking_day} | {self.team} | {self.system} | {self.rank}'



class Game(models.Model):
    ''' Represents a Mens NCAA Basketball game '''
    GT_CHOICES = (('Regular','Regular'),('NCAA','NCAA'),('Secondary','Secondary'))
    season = models.ForeignKey('Season', on_delete=models.CASCADE)
    day = models.ForeignKey('SeasonDay', on_delete=models.CASCADE)
    city = models.ForeignKey('City', on_delete=models.CASCADE, null=True)
    gid = models.CharField(max_length=50)

    teams = models.ManyToManyField('Team')
    num_ot = models.IntegerField(null=True)
    game_type = models.CharField(choices=GT_CHOICES, max_length=10, null=True)

    class Meta:
        unique_together = ['day', 'gid']


    @property
    def has_season(self):
        try:
            return bool(self.season)
        except Season.DoesNotExist:
            return False


    @classmethod
    def update_objs(cls):
        ''' A method to update team rankings from csv '''
        path = os.path.join(settings.BASE_DATA_PATH, 'MGameCities.csv')
        df = pd.read_csv(path)
        for tup in tqdm(df.itertuples()):
            season = Season.objects.filter(year=tup.Season).first()
            day, _ = SeasonDay.objects.get_or_create(season=season, day_num=tup.DayNum)
            city = City.objects.filter(kid=tup.CityID).first()
            gid = f'{tup.WTeamID}_{tup.LTeamID}'
            t1 = Team.objects.filter(kid=tup.WTeamID).first()
            t2 = Team.objects.filter(kid=tup.LTeamID).first()
            obj, _ = cls.objects.update_or_create(
                day=day, gid=gid,
                defaults=dict(season=season, game_type=tup.CRType, city=city)
            )
            obj.teams.add(*[t1,t2])
            
    def get_season(self):
        ''' A method to derive the season from the day '''
        if self.day and not self.has_season:
            self.season = self.day.season

    def get_teams(self):
        ''' A method to derive teams from gid '''
        kid1 = self.gid.split('_')[0]
        kid2 = self.gid.split('_')[1]
        team1 = Team.objects.filter(kid=kid1).first()
        team2 = Team.objects.filter(kid=kid2).first()
        self.teams.add(*[team1, team2])


    def save(self, *args, **kwargs):
        self.get_season()
        super().save(*args, **kwargs)
        self.get_teams()

    def __str__(self):
        return f'{self.day} | {self.teams.all()}'


class GameTeam(models.Model):
    ''' Represents a Game as it relates to a participating team '''
    RESULT_CHOICES = (('win','Win'),('loss','Loss'))
    LOC_CHOICES = (('H', 'Home'), ('A', 'Away'), ('N','Neutral'))
    game = models.ForeignKey('Game', on_delete=models.CASCADE)
    team = models.ForeignKey('Team', on_delete=models.CASCADE, related_name='gameteam_set')
    opponent = models.ForeignKey('Team', on_delete=models.CASCADE, related_name='gameteam_opp_set')
    loc = models.CharField(choices=LOC_CHOICES, max_length=10)
    result = models.CharField(choices=RESULT_CHOICES, max_length=10)

    class Meta:
        unique_together = ['game', 'team']

    @staticmethod
    def df_generator():
        files = ['MRegularSeasonDetailedResults.csv', 'MNCAATourneyDetailedResults.csv']
        for fn in files:
            path = os.path.join(settings.BASE_DATA_PATH, fn)
            yield pd.read_csv(path)

    @classmethod
    def update_objs(cls):
        for df in cls.df_generator():
            cls.process_df(df)
        
    @classmethod
    def process_df(cls, df):
        ''' Class method to update objs from df produced by Kaggle csv '''
        for tup in tqdm(df.itertuples()):
            season = Season.objects.get(year=tup.Season)
            day, _ = SeasonDay.objects.get_or_create(season=season, day_num=tup.DayNum)
            gid = f'{tup.WTeamID}_{tup.LTeamID}'
            game, _ = Game.objects.update_or_create(
                day=day, gid=gid,
                defaults=dict(num_ot=tup.NumOT)
            )

            wteam = Team.objects.get(kid=tup.WTeamID)
            lteam = Team.objects.get(kid=tup.LTeamID)

            wloc = tup.WLoc
            if wloc == 'H':
                lloc = 'A'
            elif wloc == 'A':
                lloc = 'H'
            else:
                lloc = 'N'

            wgt, _ = GameTeam.objects.update_or_create(
                game=game, team=wteam,
                defaults=dict(
                    loc=wloc, opponent=lteam, result='win'
                )
            )
            lgt, _ = GameTeam.objects.update_or_create(
                game=game, team=lteam,
                defaults=dict(
                    loc=lloc, opponent=wteam, result='loss'
                )
            )

            for gs in GameStat.objects.all():
                wval = getattr(tup, f'W{gs.code}')
                lval = getattr(tup, f'L{gs.code}')

                wgts = GameTeamStat.objects.update_or_create(
                    gameteam=wgt, stat=gs, opp_stat=False,
                    defaults=dict(value=wval)
                )
                wgtso = GameTeamStat.objects.update_or_create(
                    gameteam=wgt, stat=gs, opp_stat=True,
                    defaults=dict(value=lval)
                )

                lgts = GameTeamStat.objects.update_or_create(
                    gameteam=lgt, stat=gs, opp_stat=False,
                    defaults=dict(value=lval)
                )
                lgtso = GameTeamStat.objects.update_or_create(
                    gameteam=lgt, stat=gs, opp_stat=True,
                    defaults=dict(value=wval)
                )

    def __str__(self):
        return f'{self.game} | {self.team}'

class GameStat(models.Model):
    ''' Represents a stat that can be given a value for any particular game '''
    code = models.CharField(max_length=50, unique=True)
    desc =models.CharField(max_length=200)

    @classmethod
    def update_objs(cls):
        ''' A method to update game stats from csv '''
        path = os.path.join(settings.BASE_DATA_PATH, 'game_stats.csv')
        df = pd.read_csv(path)
        for tup in tqdm(df.itertuples()):
            obj, _ = cls.objects.update_or_create(
                code = tup.code, defaults=dict(desc=tup.desc)
            )

    def __str__(self):
        return f'{self.code} | {self.desc}'


class GameTeamStat(models.Model):
    ''' Represents a stat value for a given GameTeam '''
    class Meta:
        unique_together = ['gameteam', 'stat', 'opp_stat']
    
    gameteam = models.ForeignKey('GameTeam', on_delete=models.CASCADE)
    stat = models.ForeignKey('GameStat', on_delete=models.CASCADE)
    opp_stat = models.BooleanField(verbose_name='Opponent Stat Flag')
    value = models.FloatField()