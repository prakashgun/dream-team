from django.db import models


class Tournament(models.Model):
    name = models.CharField(max_length=100, blank=False, null=False, unique=True)

    def __str__(self):
        return self.name


class Ground(models.Model):
    name = models.CharField(max_length=100, blank=False, null=False, unique=True)

    def __str__(self):
        return self.name


class Team(models.Model):
    name = models.CharField(max_length=100, blank=False, null=False, unique=True)

    def __str__(self):
        return self.name


class PlayerType(models.Model):
    name = models.CharField(max_length=100, blank=False, null=False, unique=True)

    def __str__(self):
        return self.name


class MatchType(models.Model):
    name = models.CharField(max_length=100, blank=False, null=False, unique=True)

    def __str__(self):
        return self.name


class BattingStyle(models.Model):
    name = models.CharField(max_length=100, blank=False, null=False, unique=True)

    def __str__(self):
        return self.name


class BowlingStyle(models.Model):
    name = models.CharField(max_length=100, blank=False, null=False, unique=True)

    def __str__(self):
        return self.name


class Player(models.Model):
    name = models.CharField(max_length=100, blank=False, null=False, unique=True)
    dob = models.DateField()
    player_type = models.ForeignKey(PlayerType, on_delete=models.PROTECT)
    batting_style = models.ForeignKey(BattingStyle, on_delete=models.PROTECT)
    bowling_style = models.ForeignKey(BowlingStyle, on_delete=models.PROTECT)
    crawl_id = models.IntegerField()


class PlayerStats(models.Model):
    player = models.ForeignKey(Player, on_delete=models.PROTECT)
    match_type = models.ForeignKey(MatchType, on_delete=models.CASCADE)
    matches = models.IntegerField()
    innings = models.IntegerField()
    not_outs = models.IntegerField()
    runs = models.IntegerField()
    highest_score = models.IntegerField()
    average = models.FloatField()
    balls = models.IntegerField()
    strike_rate = models.FloatField()
    hundreds = models.IntegerField()
    fifties = models.IntegerField()
    fours = models.IntegerField()
    sixes = models.IntegerField()
    catches = models.IntegerField()
    stumpings = models.IntegerField()
    bowl_innings = models.IntegerField()
    bowl_balls = models.IntegerField()
    bowl_runs = models.IntegerField()
    bowl_wickets = models.IntegerField()
    bowl_best_innings = models.IntegerField()
    bowl_best_match = models.IntegerField()
    bowl_average = models.IntegerField()
    bowl_economy = models.IntegerField()
    bowl_stike_rate = models.IntegerField()
    bowl_four_wickets = models.IntegerField()
    bowl_five_wickets = models.IntegerField()
    bowl_ten_wickets = models.IntegerField()

    def __str__(self):
        return f'{self.player}-{self.match_type}'


class Match(models.Model):
    tournament = models.ForeignKey(Tournament, on_delete=models.PROTECT)
    match_type = models.ForeignKey(MatchType, on_delete=models.CASCADE)
    ground = models.ForeignKey(Ground, on_delete=models.PROTECT)
    batting_first = models.ForeignKey(Team, on_delete=models.PROTECT)
    bowling_first = models.ForeignKey(Team, on_delete=models.PROTECT)
    match_date = models.DateField()

    def __str__(self):
        return f'{self.tournament}-{self.match_type}-{self.ground}'


class MatchStats(models.Model):
    match = models.ForeignKey(Match, on_delete=models.CASCADE)
    player = models.ForeignKey(Player, on_delete=models.PROTECT)
    team = models.ForeignKey(Team, on_delete=models.PROTECT)
    opposite_team = models.ForeignKey(Team, on_delete=models.PROTECT)
    batted = models.BooleanField()
    bowled = models.BooleanField()
    bat = models.IntegerField()
    bowl = models.IntegerField()
