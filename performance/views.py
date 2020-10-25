from datetime import datetime
from time import sleep
from urllib.parse import urlparse
import os
from rest_framework.response import Response
from rest_framework.views import APIView

from .crawlers import CricInfoPlayer, CricInfoException
from .models import (Player, PlayerType, BattingStyle, BowlingStyle, PlayerStats, Team, MatchType, Ground,
                     Tournament, MatchStats, Match)
from .serializers import CrawlInfoSerializer
import csv
from .predict import Predict


class CrawlInfoView(APIView):
    def get(self, request):
        return Response(
            {
                'message': "Input data in post"
            }
        )

    def _crawl(self, crawl_id):
        try:
            cricinfo = CricInfoPlayer(crawl_id)
            name, full_name, born, player_type_name, batting_style_name, bowling_style_name = cricinfo.get_player_details()

            if not all((name, full_name, born, player_type_name, batting_style_name, bowling_style_name)):
                return False

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
                bowl_average, bowl_economy, bowl_strike_rate, bowl_four_wickets, bowl_five_wickets, bowl_ten_wickets
            ) = cricinfo.get_bowling_stats()

            tournament_name = 'IPL 2020'
            tournament, _ = Tournament.objects.get_or_create(name=tournament_name)
            current_team = None
            current_match_type = None

            for match_details in cricinfo.get_match_stats():
                (team_name, opposite_team_name, batted, bowled, not_out, runs, runs_given, wickets, ground_name,
                 match_date_str,
                 match_type_name) = match_details

                if not team_name or not match_type_name:
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
                    bowl_strike_rate=float(bowl_strike_rate),
                    bowl_four_wickets=bowl_four_wickets,
                    bowl_five_wickets=bowl_five_wickets,
                    bowl_ten_wickets=bowl_ten_wickets
                )
        except CricInfoException as e:
            return False
        except TypeError as e:
            return False

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


class PredictView(APIView):

    def get(self, request):

        return Response(
            {
                'message': "Input data for output"
            }
        )

    def _age_days_from_born(self, born):
        if not born:
            return None
        dob = datetime.strptime(','.join(born.split(',')[:2]), '%B %d, %Y')
        return abs((datetime.now() - dob).days)

    def _calculate_points(self, runs, wickets):
        return runs + wickets * 25

    def post(self, request):
        # Validate the incoming input (provided through query parameters)
        serializer = CrawlInfoSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        # Get the model input
        data = serializer.validated_data

        player_rows = []

        for url in data['urls']:
            crawl_id = os.path.basename(urlparse(url).path).replace('.html', '')
            players = Player.objects.filter(crawl_id=crawl_id)
            if not players:
                continue

            player = players[0]
            bowling_style = player.bowling_style.id if player.bowling_style else None
            match_stats = MatchStats.objects.all()
            player_stats_rows = PlayerStats.objects.filter(player=player)

            # return Response({
            #     'result': f'comes here first {player.name}'
            # })

            if not player_stats_rows:
                continue

            # return Response({
            #     'result': 'comes here'
            # })

            player_stats = player_stats_rows[0]

            if not player_stats:
                continue

            bowl_best_innings = int(
                player_stats.bowl_best_innings.split('/')[0]) if player_stats.bowl_best_innings else 0

            points = Predict.predict_points(
                player.id,
                self._age_days_from_born(player.born),
                player.player_type.id,
                player.batting_style.id,
                 bowling_style,
                 1,
                 3,
                 8,
                 player_stats.matches,
                 player_stats.innings,
                 player_stats.not_outs,
                 player_stats.runs,
                 int(player_stats.highest_score.replace('*', '')),
                 player_stats.average,
                 player_stats.balls,
                 player_stats.strike_rate,
                 player_stats.hundreds,
                 player_stats.fifties,
                 player_stats.fours,
                 player_stats.sixes,
                 player_stats.catches,
                 player_stats.stumpings,
                 player_stats.bowl_innings,
                 player_stats.bowl_balls,
                 player_stats.bowl_runs,
                 player_stats.bowl_wickets,
                 bowl_best_innings,
                 player_stats.bowl_average,
                 player_stats.bowl_economy,
                 player_stats.bowl_strike_rate,
                 player_stats.bowl_four_wickets,
                 player_stats.bowl_five_wickets
            )

            row = {
                'player_name': Player.name,
                'points': points
            }
            player_rows.append(row)



        return Response({
            'result': player_rows
        })


class GivePrediction(APIView):

    def get(self, request):

        return Response(
            {
                'message': "Input data for output"
            }
        )

    def _age_days_from_born(self, born):
        if not born:
            return None
        dob = datetime.strptime(','.join(born.split(',')[:2]), '%B %d, %Y')
        return abs((datetime.now() - dob).days)

    def _calculate_points(self, runs, wickets):
        return runs + wickets * 25

    def post(self, request):
        # Validate the incoming input (provided through query parameters)
        serializer = CrawlInfoSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        # Get the model input
        data = serializer.validated_data

        player_rows = []

        players = Player.objects.all()

        for player in players:
            bowling_style = player.bowling_style.id if player.bowling_style else None
            match_stats = MatchStats.objects.all()
            player_stats_rows = PlayerStats.objects.filter(player=player)

            if not player_stats_rows:
                continue

            player_stats = player_stats_rows[0]

            if not player_stats:
                continue

            bowl_best_innings = int(
                player_stats.bowl_best_innings.split('/')[0]) if player_stats.bowl_best_innings else 0

            for match_stat in match_stats:
                row = {
                    'id': player.id,
                    'age_days': self._age_days_from_born(player.born),
                    'player_type': player.player_type.id,
                    'batting_style': player.batting_style.id,
                    'bowling_style': bowling_style,
                    'ground': match_stat.match.ground.id,
                    'opposite_team': match_stat.opposite_team.id,
                    'current_team': match_stat.team.id,
                    'matches': player_stats.matches,
                    'innings': player_stats.innings,
                    'not_outs': player_stats.not_outs,
                    'runs': player_stats.runs,
                    'highest_score': int(player_stats.highest_score.replace('*', '')),
                    'average': player_stats.average,
                    'balls': player_stats.balls,
                    'strike_rate': player_stats.strike_rate,
                    'hundreds': player_stats.hundreds,
                    'fifties': player_stats.fifties,
                    'fours': player_stats.fours,
                    'sixes': player_stats.sixes,
                    'catches': player_stats.catches,
                    'stumpings': player_stats.stumpings,
                    'bowl_innings': player_stats.bowl_innings,
                    'bowl_balls': player_stats.bowl_balls,
                    'bowl_runs': player_stats.bowl_runs,
                    'bowl_wickets': player_stats.bowl_wickets,
                    'bowl_best_innings': bowl_best_innings,
                    'bowl_average': player_stats.bowl_average,
                    'bowl_economy': player_stats.bowl_economy,
                    'bowl_strike_rate': player_stats.bowl_strike_rate,
                    'bowl_four_wickets': player_stats.bowl_four_wickets,
                    'bowl_five_wickets': player_stats.bowl_five_wickets,
                    'points': self._calculate_points(match_stat.runs, match_stat.wickets)
                }

                player_rows.append(row)

        with open('player_rows.csv', 'w') as file:
            writer = csv.DictWriter(file, player_rows[0].keys())
            writer.writeheader()
            for index in player_rows:
                writer.writerow(index)

        return Response({
            'result': player_rows
        })