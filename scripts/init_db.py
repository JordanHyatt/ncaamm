from main.models import *


def run(*args):
    City.update_objs()
    Conference.update_objs()
    Team.update_objs()
    Season.update_objs()
    GameStat.update_objs()
    TeamCoach.update_objs()
    TeamConference.update_objs()
    TeamRank.update_objs()
    Game.update_objs()
    GameTeam.update_objs()
    TourneySeed.update_objs()
