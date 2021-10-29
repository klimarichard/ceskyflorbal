import datetime
import re
import os
import requests
from bs4 import BeautifulSoup


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

        with open(f'aktualni/csv/stream/league_table.csv', 'w', encoding='utf-8') as f:
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

        write_table_to_file(table, f'aktualni/csv/stream/{team}_players.csv', [1, 3, 4, 5, 8, 12])
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
        print(f"Goalies stats table page for {team.upper()} opened successfully...")

        soup = BeautifulSoup(page.text, 'html.parser')

        table = soup.find('tbody', id=re.compile('^datablock-GoalieStatsDataGrid'))

        write_table_to_file(table, f'aktualni/csv/stream/{team}_goalies.csv', [1, 4, 5, 7, 12])
    else:
        print(f'ERROR: Unsuccessful loading of goalies stats table page for {team.upper()}!')


def get_abbr_team_name(team):
    """
    Gets abbreviated team name from the full one.
    :param team: full team name
    :return: abbreviated team name
    """
    for key, value in TEAMS_FULLNAMES.items():
        if team == value:
            return key

    return 'ERROR: Wrong team abbreviation'


def write_table_to_file(table, filename: str, indexes):
    """
    Writes contents of given table to file.
    :param table: HTML table with data
    :param filename: name of the file
    :param indexes: list of indexes of data desired in the output
    :return: nothing
    """
    with open(filename, 'w', encoding='utf-8') as f:
        for tr in table.find_all('tr'):
            s = read_cells_in_row(tr, indexes)
            f.write(s)


def read_cells_in_row(row, indexes):
    """
    Reads all cells in a given row of some table.
    :param row: row of HTML table (<c><tr></c>)
    :param indexes: list of indexes of data desired in the output
    :return: string with row data
    """
    s = ''
    tds = row.find_all('td')

    for i in indexes:
        if ',' in tds[i].text.strip():
            s = s + '"' + tds[i].text.strip() + '"'
        else:
            s += tds[i].text.strip()
        s += ','

    s += extract_player_ID(tds[1])

    s = s[:-1] + '\n'

    return s


def extract_player_ID(td):
    """
    Extract ID part of the link to player page.
    :param td: a cell with the link in it
    :return: ID part of the link
    """
    a = td.find('a', href=True)

    return a['href'][7:]


def get_team_abbr(team_full_name):
    """
    Get abbreviated name of a team from its full name.
    :param team_full_name: full name of the team
    :return: abbreviated name for this team
    """
    for key, value in TEAMS_FULLNAMES.items():
        if team_full_name == value:
            return key

    return 'WRONG TEAM NAME'


def main():
    """
    Main function of the script.
    :return: nothing
    """
    # checks if current csv directory exists, if not, creates it
    if not os.path.exists(f'aktualni/csv/stream'):
        os.makedirs(f'aktualni/csv/stream')

    read_league_table()

    for team in TEAMS_DICT.keys():
        print('-------------------------------')
        read_team_players_stats(team)
        read_team_goalies_stats(team)


TABLE = r'https://www.ceskyflorbal.cz/superliga-muzi/tabulka'
BASE_URL = r'https://www.ceskyflorbal.cz/druzstvo/'
TEAMS_DICT = {'VIT': '30499', 'MB': '29996', 'TAT': '29533', 'BOH': '30768', 'CHO': '30856', 'OST': '30324',
              'SPA': '30593', 'BA': '30982', 'LIB': '29635', 'HAT': '30236', 'CLP': '28896', 'PAR': '30011',
              'OTR': '29805', 'SKV': '30416'}
TEAMS_PLAYOFF_DICT = {'VIT': '27231', 'MB': '27929', 'TAT': '26841', 'BOH': '28310', 'CHO': '26151', 'OST': '26682',
                      'SPA': '26345', 'BA': '28078'}
TEAMS_FULLNAMES = {'VIT': '1. SC TEMPISH Vítkovice', 'MB': 'Předvýběr.CZ Florbal MB',
                   'TAT': 'Tatran Střešovice', 'BOH': 'FbŠ Bohemians', 'CHO': 'FAT PIPE FLORBAL CHODOV',
                   'OST': 'FBC ČPP OSTRAVA', 'SPA': 'ACEMA Sparta Praha', 'BA': 'BLACK ANGELS', 'LIB': 'FBC Liberec',
                   'HAT': 'FBŠ Hummel Hattrick Brno', 'CLP': 'FBC 4CLEAN Česká Lípa', 'PAR': 'SOKOLI Pardubice',
                   'OTR': 'Navláčil PANTHERS OTROKOVICE', 'SKV': 'TJ Sokol Královské Vinohrady'}
SEASON_FIRST_YEAR = 21
SEASON_SECOND_YEAR = 22

if __name__ == '__main__':
    main()
