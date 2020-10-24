from datetime import datetime
from time import sleep
from urllib.parse import urlparse
import os
from rest_framework.response import Response
from rest_framework.views import APIView

from .crawlers import CricInfoPlayer
from .models import (Player, PlayerType, BattingStyle, BowlingStyle, PlayerStats, Team, MatchType, Ground,
                     Tournament, MatchStats, Match)
from .serializers import CrawlInfoSerializer


class CrawlInfoView(APIView):
    def get(self, request):
        return Response(
            {
                'message': "Input data in post"
            }
        )

    def _crawl(self, crawl_id):
        cricinfo = CricInfoPlayer(crawl_id)
        name, full_name, born, player_type_name, batting_style_name, bowling_style_name = cricinfo.get_player_details()

        player_type, _ = PlayerType.objects.get_or_create(name=player_type_name)
        batting_style, _ = BattingStyle.objects.get_or_create(name=batting_style_name)
        if bowling_style_name:
            bowling_style, _ = BowlingStyle.objects.get_or_create(name=bowling_style_name)
        else:
            bowling_style = None

        player, _ = Player.objects.get_or_create(
            name=name, born=born, player_type=player_type, batting_style=batting_style,
            bowling_style=bowling_style, crawl_id=crawl_id
        )

        (
            matches, innings, not_outs, runs, highest_score, average, balls, strike_rate, hundreds, fifties, fours,
            sixes, catches, stumpings
        ) = cricinfo.get_batting_stats()

        (
            bowl_innings, bowl_balls, bowl_runs, bowl_wickets, bowl_best_innings, bowl_best_match,
            bowl_average, bowl_economy, bowl_stike_rate, bowl_four_wickets, bowl_five_wickets, bowl_ten_wickets
        ) = cricinfo.get_bowling_stats()

        tournament_name = 'IPL 2020'
        tournament, _ = Tournament.objects.get_or_create(name=tournament_name)
        current_team = None
        current_match_type = None

        for match_details in cricinfo.get_match_stats():
            (team_name, opposite_team_name, batted, bowled, not_out, runs, runs_given, wickets, ground_name,
             match_date_str,
             match_type_name) = match_details

            if not team_name or match_type_name:
                continue

            team, _ = Team.objects.get_or_create(name=team_name)

            opposite_team, _ = Team.objects.get_or_create(name=opposite_team_name)
            ground, _ = Ground.objects.get_or_create(name=ground_name)
            match_date = datetime.strptime(match_date_str, '%d %b %Y')
            match_type, _ = MatchType.objects.get_or_create(name=match_type_name)

            if team:
                current_team = team

            if match_type:
                current_match_type = match_type

            match, _ = Match.objects.get_or_create(
                tournament=tournament,
                match_type=match_type,
                ground=ground,
                match_date=match_date
            )

            match_stats, _ = MatchStats.objects.get_or_create(
                match=match,
                player=player,
                team=team,
                opposite_team=opposite_team,
                batted=batted,
                bowled=bowled,
                not_out=not_out,
                runs=runs,
                runs_given=runs_given,
                wickets=wickets
            )

        if current_team and current_match_type:
            player_stats, _ = PlayerStats.objects.get_or_create(
                player=player,
                match_type=current_match_type,
                current_team=current_team,
                matches=matches,
                innings=innings,
                not_outs=not_outs,
                runs=runs,
                highest_score=highest_score,
                average=float(average),
                balls=balls,
                strike_rate=float(strike_rate),
                hundreds=hundreds,
                fifties=fifties,
                fours=fours,
                sixes=sixes,
                catches=catches,
                stumpings=stumpings,
                bowl_innings=bowl_innings,
                bowl_balls=bowl_balls,
                bowl_runs=bowl_runs,
                bowl_wickets=bowl_wickets,
                bowl_best_innings=bowl_best_innings,
                bowl_best_match=bowl_best_match,
                bowl_average=float(bowl_average),
                bowl_economy=float(bowl_economy),
                bowl_stike_rate=float(bowl_stike_rate),
                bowl_four_wickets=bowl_four_wickets,
                bowl_five_wickets=bowl_five_wickets,
                bowl_ten_wickets=bowl_ten_wickets
            )

    def post(self, request):
        # Validate the incoming input (provided through query parameters)
        serializer = CrawlInfoSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        # Get the model input
        data = serializer.validated_data

        for url in data['urls']:
            crawl_id = os.path.basename(urlparse(url).path).replace('.html', '')
            sleep(5)
            self._crawl(crawl_id)

        return Response({
            'result': 'Crawled'
        })
