from django.db.models.signals import post_save, post_delete, pre_delete
from django.dispatch import receiver
from main.models import *


################ Finance Upload Signals ##############
##########################################################
@receiver(post_save, sender=Season)
def create_season_days(sender,instance,created=False,**kwargs):
    for i in range(0,201):
        SeasonDay.objects.get_or_create(season=instance, day_num=i)