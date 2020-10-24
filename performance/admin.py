from django.contrib import admin

from .models import Player, PlayerType, PlayerStats, MatchType, MatchStats, Match, Tournament, Ground, Team, \
    BowlingStyle, BattingStyle

admin.site.register(Player)
admin.site.register(PlayerType)
admin.site.register(PlayerStats)
admin.site.register(MatchStats)
admin.site.register(Match)
admin.site.register(MatchType)
admin.site.register(Tournament)
admin.site.register(Ground)
admin.site.register(Team)
admin.site.register(BowlingStyle)
admin.site.register(BattingStyle)
