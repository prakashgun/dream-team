from django.db import models


class Tournament(models.Model):
    objects = models.Manager()
    name = models.CharField(max_length=100, blank=False, null=False, unique=True)

    def __str__(self):
        return self.name


class Ground(models.Model):
    objects = models.Manager()
    name = models.CharField(max_length=100, blank=False, null=False, unique=True)

    def __str__(self):
        return self.name


class Team(models.Model):
    objects = models.Manager()
    name = models.CharField(max_length=100, blank=False, null=False, unique=True)

    def __str__(self):
        return self.name


class PlayerType(models.Model):
    objects = models.Manager()
    name = models.CharField(max_length=100, blank=False, null=False, unique=True)

    def __str__(self):
        return self.name


class MatchType(models.Model):
    objects = models.Manager()
    name = models.CharField(max_length=100, blank=False, null=False, unique=True)

    def __str__(self):
        return self.name


class BattingStyle(models.Model):
    objects = models.Manager()
    name = models.CharField(max_length=100, blank=False, null=False, unique=True)

    def __str__(self):
        return self.name


class BowlingStyle(models.Model):
    objects = models.Manager()
    name = models.CharField(max_length=100, blank=False, null=False, unique=True)

    def __str__(self):
        return self.name


class Player(models.Model):
    objects = models.Manager()
    name = models.CharField(max_length=100, blank=False, null=False, unique=True)
    born = models.CharField(max_length=100, blank=False, null=False)
    player_type = models.ForeignKey(PlayerType, on_delete=models.PROTECT)
    batting_style = models.ForeignKey(BattingStyle, on_delete=models.PROTECT)
    bowling_style = models.ForeignKey(BowlingStyle, on_delete=models.PROTECT, blank=True, null=True)
    crawl_id = models.IntegerField()

    def __str__(self):
        return self.name


class PlayerStats(models.Model):
    objects = models.Manager()
    player = models.ForeignKey(Player, on_delete=models.PROTECT)
    match_type = models.ForeignKey(MatchType, on_delete=models.CASCADE)
    current_team = models.ForeignKey(Team, on_delete=models.PROTECT, blank=True, null=True)
    matches = models.IntegerField()
    innings = models.IntegerField()
    not_outs = models.IntegerField()
    runs = models.IntegerField()
    highest_score = models.CharField(max_length=10)
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
    bowl_best_innings = models.CharField(max_length=100)
    bowl_best_match = models.CharField(max_length=100)
    bowl_average = models.FloatField()
    bowl_economy = models.IntegerField()
    bowl_strike_rate = models.IntegerField()
    bowl_four_wickets = models.IntegerField()
    bowl_five_wickets = models.IntegerField()
    bowl_ten_wickets = models.IntegerField()

    class Meta:
        unique_together = ('player', 'match_type')

    def __str__(self):
        return f'{self.player}-{self.match_type}'


class Match(models.Model):
    objects = models.Manager()
    tournament = models.ForeignKey(Tournament, on_delete=models.PROTECT)
    match_type = models.ForeignKey(MatchType, on_delete=models.CASCADE)
    ground = models.ForeignKey(Ground, on_delete=models.PROTECT)
    # batting_first = models.ForeignKey(Team, on_delete=models.PROTECT, related_name='match_batting_first')
    # bowling_first = models.ForeignKey(Team, on_delete=models.PROTECT, related_name='match_bowling_first')
    match_date = models.DateField()

    class Meta:
        unique_together = ('tournament', 'match_type', 'ground', 'match_date')

    def __str__(self):
        return f'{self.tournament}-{self.match_type}-{self.ground}'


class MatchStats(models.Model):
    objects = models.Manager()
    match = models.ForeignKey(Match, on_delete=models.CASCADE)
    player = models.ForeignKey(Player, on_delete=models.PROTECT)
    team = models.ForeignKey(Team, on_delete=models.PROTECT, related_name='match_stats_team')
    opposite_team = models.ForeignKey(Team, on_delete=models.PROTECT, related_name='match_stats_opposite_team')
    batted = models.BooleanField()
    bowled = models.BooleanField()
    not_out = models.BooleanField()
    runs = models.IntegerField()
    runs_given = models.IntegerField()
    wickets = models.IntegerField()

    class Meta:
        unique_together = ('match', 'player')

