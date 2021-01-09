import requests
from bs4 import BeautifulSoup
import re


def read_league_table():
    """
    Reads league team stats.
    :return: nothing
    """
    url = TABLE
    page = requests.get(url)

    # if opening the page was OK
    if page.status_code == 200:
        print("League table page opened successfully...")

        soup = BeautifulSoup(page.text, 'html.parser')

        table = soup.find('tbody', id=re.compile('^datablock-TeamStatsDataGrid_'))

        with open('csv_2021/tabulka.csv', 'w', encoding='utf-8') as f:
            for tr in table.find_all('tr'):
                s = ''
                for td in tr.find_all('td'):
                    s += td.text.strip()
                    s += ','

                s = s[:-1] + '\n'
                f.write(s)
    else:
        print(f'ERROR: Unsuccessful loading of league table page!')


def read_team_players_stats(team: str):
    """
    Reads stats of all players from given team.
    :param team: team abbreviated name
    :return: nothing
    """
    page = requests.get(BASE_URL + TEAMS_DICT[team] + '/statistiky/hraci')

    # if opening page was OK
    if page.status_code == 200:
        print(f"Players stats table page for {team.upper()} opened successfully...")

        soup = BeautifulSoup(page.text, 'html.parser')

        table = soup.find('tbody', id=re.compile('^datablock-PlayerStatsDataGrid'))

        with open(f'csv_2021/{team}_players.csv', 'w', encoding='utf-8') as f:
            for tr in table.find_all('tr'):
                s = ''
                for td in tr.find_all('td'):
                    s += td.text.strip()
                    s += ','

                s = s[:-1] + '\n'
                f.write(s)
    else:
        print(f'ERROR: Unsuccessful loading of players stats table page for {team.upper()}!')


def read_team_goalies_stats(team: str):
    """
    Reads stats of all goalies from given team.
    :param team: team abbreviated name
    :return: nothing
    """
    page = requests.get(BASE_URL + TEAMS_DICT[team] + '/statistiky/brankari')

    # if opening page was OK
    if page.status_code == 200:
        print(f"Players stats table page for {team.upper()} opened successfully...")

        soup = BeautifulSoup(page.text, 'html.parser')

        table = soup.find('tbody', id=re.compile('^datablock-GoalieStatsDataGrid'))

        with open(f'csv_2021/{team}_goalies.csv', 'w', encoding='utf-8') as f:
            for tr in table.find_all('tr'):
                s = ''
                for td in tr.find_all('td'):
                    s += td.text.strip()
                    s += ','

                s = s[:-1] + '\n'
                f.write(s)
    else:
        print(f'ERROR: Unsuccessful loading of players stats table page for {team.upper()}!')


def read_team_bestof_stats(team):
    """
    Reads best-of statistics of given team.
    :param team: team abbreviated name
    :return: nothing
    """
    page = requests.get(BASE_URL + TEAMS_DICT[team] + '/statistiky')

    # if opening page was OK
    if page.status_code == 200:
        print(f"Best-of stats table page for {team.upper()} opened successfully...")

        soup = BeautifulSoup(page.text, 'html.parser')

        tables = soup.findAll('table', {'class': 'statTable'})

        for i in range(len(tables)):
            with open(f'csv_2021/{team}_{BEST_OF_ORDER[i]}.csv', 'w', encoding='utf-8') as f:
                for tr in tables[i].find_all('tr'):
                    s = ''
                    for td in tr.find_all('td'):
                        s += td.text.strip()
                        s += ','

                    s = s[:-1] + '\n'
                    f.write(s)
    else:
        print(f'ERROR: Unsuccessful loading of players stats table page for {team.upper()}!')


TABLE = r'https://www.ceskyflorbal.cz/superliga-muzi/tabulka'
BASE_URL = r'https://www.ceskyflorbal.cz/druzstvo/'
TEAMS_DICT = {'vitkovice': '27231', 'boleslav': '27929', 'tatran': '26841', 'bohemians': '28310',
              'chodov': '26151', 'ostrava': '26682', 'sparta': '26345', 'ba': '28078', 'liberec': '26709',
              'hattrick': '27660', 'clipa': '28266', 'pardubice': '28194', 'otrokovice': '26086',
              'skv': '26475'}
BEST_OF_ORDER = ['body', 'prumer', 'goly', 'vyhry', 'asistence', 'tm']

read_league_table()

for team in TEAMS_DICT.keys():
    print('-------------------------------')
    read_team_players_stats(team)
    read_team_goalies_stats(team)
    read_team_bestof_stats(team)
