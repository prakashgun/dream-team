import requests
from lxml import html


class CricInfoPlayer:

    def __init__(self, crawl_id):
        self.crawl_id = crawl_id

    def get_player_link(self):
        return f'https://www.espncricinfo.com/india/content/player/{self.crawl_id}.html'

    def player_info_path(self, index):
        return f'//*[@class ="ciPlayerinformationtxt"][{index}]/span'

    def player_stat_path(self, first_index, second_index, third_index):
        return f'//*[@class ="engineTable"][{first_index}]/tbody/tr[{second_index}]/td[{third_index}]'

    def get_crawled_content(self, path):
        response = requests.get(self.get_player_link())
        byte_string = response.content

        # with open('/home/prakash/Documents/code/practice/python/lxml/shami.html') as f:
        #     content = f.read()
        # byte_string = content

        # get filtered source code
        source_code = html.fromstring(byte_string)
        # jump to preferred html element
        tree = source_code.xpath(path)

        if not tree:
            return None

        value = tree[0].text_content().strip()

        return value if value != '-' else 0

    def get_player_details(self):

        full_name = None
        born = None
        player_type = None
        batting_style = None
        bowling_style = None

        path = '//*[@class ="ciPlayernametxt"]/div / h1[1]'
        name = self.get_crawled_content(path=path)

        for index in range(1, 10):
            path = f'//*[@class ="ciPlayerinformationtxt"][{index}]/b'
            title = self.get_crawled_content(path)

            if title == 'Full name':
                full_name = self.get_crawled_content(self.player_info_path(index))
            elif title == 'Born':
                born = self.get_crawled_content(self.player_info_path(index))
            elif title == 'Playing role':
                playing_role = self.get_crawled_content(self.player_info_path(index)).lower()

                if 'allrounder' in playing_role:
                    player_type = 'Allrounder'
                elif 'bowler' in playing_role or 'bowling' in playing_role:
                    player_type = 'Bowler'
                elif 'batting' in playing_role or 'batsman' in playing_role:
                    player_type = 'Batsman'
                else:
                    raise Exception('Player type cannot be determined')

            elif title == 'Batting style':
                batting_style = self.get_crawled_content(self.player_info_path(index))
            elif title == 'Bowling style':
                bowling_style = self.get_crawled_content(self.player_info_path(index))

        return name, full_name, born, player_type, batting_style, bowling_style

    def get_batting_stats(self):
        for index in range(10):
            engine_table_index = 1
            path = f'//*[@class ="engineTable"][{engine_table_index}]/tbody/tr[{index}]/td'

            match_type = self.get_crawled_content(path)

            if match_type != 'T20s':
                continue

            matches = self.get_crawled_content(self.player_stat_path(engine_table_index, index, 2))
            innings = self.get_crawled_content(self.player_stat_path(engine_table_index, index, 3))
            not_outs = self.get_crawled_content(self.player_stat_path(engine_table_index, index, 4))
            runs = self.get_crawled_content(self.player_stat_path(engine_table_index, index, 5))
            highest_score = self.get_crawled_content(self.player_stat_path(engine_table_index, index, 6))
            average = self.get_crawled_content(self.player_stat_path(engine_table_index, index, 7))
            balls = self.get_crawled_content(self.player_stat_path(engine_table_index, index, 8))
            strike_rate = self.get_crawled_content(self.player_stat_path(engine_table_index, index, 9))
            hundreds = self.get_crawled_content(self.player_stat_path(engine_table_index, index, 10))
            fifties = self.get_crawled_content(self.player_stat_path(engine_table_index, index, 11))
            fours = self.get_crawled_content(self.player_stat_path(engine_table_index, index, 12))
            sixes = self.get_crawled_content(self.player_stat_path(engine_table_index, index, 13))
            catches = self.get_crawled_content(self.player_stat_path(engine_table_index, index, 14))
            stumpings = self.get_crawled_content(self.player_stat_path(engine_table_index, index, 15))

            return (
                matches, innings, not_outs, runs, highest_score, average, balls, strike_rate, hundreds, fifties, fours,
                sixes, catches, stumpings
            )

    def get_bowling_stats(self):
        for index in range(10):
            engine_table_index = 2
            path = f'//*[@class ="engineTable"][{engine_table_index}]/tbody/tr[{index}]/td'

            match_type = self.get_crawled_content(path)

            if match_type != 'T20s':
                continue

            path = f'//*[@class ="engineTable"][2]/tbody/tr[{index}]/td[3]'

            bowl_innings = self.get_crawled_content(self.player_stat_path(engine_table_index, index, 3))
            bowl_balls = self.get_crawled_content(self.player_stat_path(engine_table_index, index, 4))
            bowl_runs = self.get_crawled_content(self.player_stat_path(engine_table_index, index, 5))
            bowl_wickets = self.get_crawled_content(self.player_stat_path(engine_table_index, index, 6))
            bowl_best_innings = self.get_crawled_content(self.player_stat_path(engine_table_index, index, 7))
            bowl_best_match = self.get_crawled_content(self.player_stat_path(engine_table_index, index, 8))
            bowl_average = self.get_crawled_content(self.player_stat_path(engine_table_index, index, 9))
            bowl_economy = self.get_crawled_content(self.player_stat_path(engine_table_index, index, 10))
            bowl_stike_rate = self.get_crawled_content(self.player_stat_path(engine_table_index, index, 11))
            bowl_four_wickets = self.get_crawled_content(self.player_stat_path(engine_table_index, index, 12))
            bowl_five_wickets = self.get_crawled_content(self.player_stat_path(engine_table_index, index, 13))
            bowl_ten_wickets = self.get_crawled_content(self.player_stat_path(engine_table_index, index, 14))

            return (
                bowl_innings, bowl_balls, bowl_runs, bowl_wickets, bowl_best_innings, bowl_best_match,
                bowl_average, bowl_economy, bowl_stike_rate, bowl_four_wickets, bowl_five_wickets, bowl_ten_wickets
            )

    def get_match_stats(self):
        matches = []

        for index in range(12):
            engine_table_index = 4
            path = f'//*[@class ="engineTable"][{engine_table_index}]/tbody/tr[{index}]/td[2]'

            team = self.get_crawled_content(path)

            teams = {
                'Capitals', 'Mum Indians', 'RCB', 'KKR', 'Sunrisers', 'Royals', 'Kings XI', 'Super Kings'
            }

            if team not in teams:
                continue

            bat_bowl = self.get_crawled_content(self.player_stat_path(engine_table_index, index, 1))
            stats = str(bat_bowl).split(',')

            batted = False
            bowled = False
            not_out = False
            runs = 0
            runs_given = 0
            wickets = 0

            for stat in stats:
                if 'c' in stat or 's' in stat:
                    continue
                if '/' in stat:
                    bowled = True
                    stat_detail = stat.split('/')
                    wickets = stat_detail[0]
                    runs_given = stat_detail[1]
                elif '*' in stat:
                    batted = True
                    not_out = True
                    runs = stat.replace('*', '')
                else:
                    batted = True
                    runs = stat

            opposite_team = self.get_crawled_content(
                self.player_stat_path(engine_table_index, index, 3)
            ).replace('v ', '')

            ground = self.get_crawled_content(self.player_stat_path(engine_table_index, index, 4))
            match_date = self.get_crawled_content(self.player_stat_path(engine_table_index, index, 5))
            match_type = self.get_crawled_content(self.player_stat_path(engine_table_index, index, 6))

            matches.append((team, opposite_team, batted, bowled, not_out, runs, runs_given, wickets, ground, match_date,
                            match_type))

        return matches
