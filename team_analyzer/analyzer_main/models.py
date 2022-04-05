from django.db import models
from django.contrib.auth.models import User
import datetime

class Tag(models.Model):
    name = models.CharField(max_length=75)

    def __str__(self):
        return self.name

class Player(models.Model):
    name = models.CharField(max_length=264)
    id = models.CharField(max_length=100, primary_key=True, unique=True)

    class Position(models.TextChoices):
        QB = 'QB'
        WR = 'WR'
        RB = 'RB'
        TE = 'TE'
        Pick = 'Pick'

    position = models.CharField(max_length=264, choices=Position.choices, default='QB')

    def __str__(self):
        return self.name

class User_Ranking(models.Model):
    name = models.CharField(max_length=75, unique=True)
    tags = models.ManyToManyField(Tag)
    date_created = models.DateField(auto_now_add=True,null=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.name

class Ranking(models.Model):
    user_ranking = models.ForeignKey(User_Ranking, null=True, on_delete=models.SET_NULL)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    player = models.ForeignKey(Player, null=True, on_delete=models.CASCADE)
    value = models.FloatField(default=0, null=True)
    date_last_updated = models.DateField(default=datetime.date.today, blank=True)

class Team(models.Model):
    team = models.CharField(max_length=25, null=True)
    league_id = models.CharField(max_length=25)
    team_name = models.CharField(max_length=25)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    user_ranking = models.ForeignKey(User_Ranking, null=True, on_delete=models.SET_NULL)
    team_ids = models.CharField(max_length=10000, null=True)

    class DraftOrder(models.TextChoices):
        Max_Points_For = 'Max Points For'
        Standings = 'Standings'

    draft_order = models.CharField(max_length=264, choices=DraftOrder.choices, default='Max Points For')

    def __str__(self):
        return self.team

class League(models.Model):
    name = models.CharField(max_length=30, null=True)
    league_id = models.CharField(max_length=30)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    user_ranking = models.ForeignKey(User_Ranking, null=True, on_delete=models.SET_NULL)

    class DraftOrder(models.TextChoices):
        Max_Points_For = 'Max Points For'
        Standings = 'Standings'

    draft_order = models.CharField(max_length=264, choices=DraftOrder.choices, default='Max Points For')

class league_output(models.Model):
    class Meta:
        db_table = 'league_output'

    player_id = models.CharField(max_length=30, null=True)
    name = models.CharField(max_length=30, null=True)
    date_last_updated = models.DateField(blank=True, null=True)
    value = models.FloatField(default=0, null=True)
    position = models.CharField(max_length=30, null=True)
    display_name = models.CharField(max_length=30, null=True)
    league_id = models.CharField(max_length=30)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    primary_id = models.CharField(max_length=250, primary_key=True, default=None)

class table_league_total(models.Model):
    class Meta:
        db_table = 'league_totalval_table'

    display_name = models.CharField(max_length=30, null=True)
    value = models.FloatField(default=0, null=True)
    league_id = models.CharField(max_length=30)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    primary_id = models.CharField(max_length=250, primary_key=True, default=None)

class Ranking_History(models.Model):
    ranking = models.ForeignKey(Ranking, on_delete=models.CASCADE)
    date = models.DateField(default=datetime.date.today, blank=True)
