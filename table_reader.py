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

        with open(f'csv_{SEASON_FIRST_YEAR}{SEASON_SECOND_YEAR}/tabulka.csv', 'w', encoding='utf-8') as f:
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

        write_table_to_file(table, f'csv_{SEASON_FIRST_YEAR}{SEASON_SECOND_YEAR}/{team}_players.csv')
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

        write_table_to_file(table, f'csv_{SEASON_FIRST_YEAR}{SEASON_SECOND_YEAR}/{team}_goalies.csv')
    else:
        print(f'ERROR: Unsuccessful loading of goalies stats table page for {team.upper()}!')


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

        write_best_of_tables_to_file(tables, f'csv_{SEASON_FIRST_YEAR}{SEASON_SECOND_YEAR}/{team}_bestof.csv')
    else:
        print(f'ERROR: Unsuccessful loading of best-of stats table page for {team.upper()}!')


def read_team_matches(team):
    """
    Read the list of matches of given team.
    :param team: team abbreviated name
    :return: nothing
    """
    page = requests.get(BASE_URL + TEAMS_DICT[team] + '/zapasy')

    # if opening page was OK
    if page.status_code == 200:
        print(f"Matches page for {team.upper()} opened successfully...")

        soup = BeautifulSoup(page.text, 'html.parser')

        table = soup.find('tbody', id=re.compile('^datablock-TeamMatchesDataGrid_'))

        matches = []

        for tr in table.find_all('tr'):
            match = []
            for td in tr.find_all('td'):
                if ',' in td.text.strip():
                    match.append('"' + td.text.strip() + '"')
                elif td.text.strip() != '':
                    match.append(td.text.strip())

            matches.append(match)

        last_5, next_5, streak = process_matches(matches, team)

        with open(f'csv_{SEASON_FIRST_YEAR}{SEASON_SECOND_YEAR}/{team}_zapasy.csv', 'w', encoding='utf-8') as f:
            for match in last_5:
                f.write(match_to_string(match, team))
            for match in next_5:
                f.write(match_to_string(match, team))
            f.write(streak)
    else:
        print(f'ERROR: Unsuccessful loading of matches page for {team.upper()}!')


def process_matches(matches, team):
    """
    Finds played matches, future matches and team streak from list of all matches.
    :param matches: list of all matches
    :param team: abbreviated team name
    :return: lists of last 5 matches, next 5 matches and a string with team streak
    """
    past = []
    future = []

    today = datetime.date.today()

    # determine past and future matches
    for match in matches:
        date_split = match[0].split('.')
        day = int(date_split[0].strip())
        month = int(date_split[1].strip())
        if month > 8:
            year = 2000 + SEASON_FIRST_YEAR
        else:
            year = 2000 + SEASON_SECOND_YEAR

        match[0] = datetime.date(year, month, day)

        if match[0] < today:
            past.append(match)
        elif match[0] > today:
            future.append(match)

    sorted(past, key=lambda record: record[0])
    sorted(future, key=lambda record: record[0])

    last_5 = []
    next_5 = []

    for i in range(len(past) - 1, max(len(past) - 6, -1), -1):
        last_5.append(past[i])

    for i in range(min(5, len(future))):
        next_5.append(future[i])

    streak = find_streak(past, team)

    return last_5, next_5, streak


def find_streak(past_matches, team):
    """
    Finds 10-match streak from past matches.
    :param past_matches: list of past matches
    :param team: abbreviated team name
    :return: string with 10 match streak
    """
    streak = []

    for i in range(max(0, len(past_matches) - 10), len(past_matches)):
        match = past_matches[i]
        score_split = match[-1].split(':')
        p = False

        home_score = int(score_split[0])
        away_score = score_split[1]

        if not away_score.isnumeric():
            p = True
            if away_score[-1] == 'p':
                away_score = int(away_score[:-1])
            elif away_score[-1] == 'n':
                away_score = int(away_score[:-2])
        else:
            away_score = int(away_score)

        if match[3] == TEAMS_FULLNAMES[team]:
            if home_score > away_score:
                if p:
                    streak.append('VP')
                else:
                    streak.append('V')
            else:
                if p:
                    streak.append('PP')
                else:
                    streak.append('P')
        elif match[4] == TEAMS_FULLNAMES[team]:
            if away_score > home_score:
                if p:
                    streak.append('VP')
                else:
                    streak.append('V')
            else:
                if p:
                    streak.append('PP')
                else:
                    streak.append('P')

    result = ''
    for j in range(len(streak)):
        result += streak[j]
        if j != len(streak) - 1:
            result += ' - '

    return result


def match_to_string(match, team):
    """
    Returns representation of the match as a .csv compatible string.
    :param match: list with match data
    :param team: abbreviated team name
    :return: string with match data
    """
    result = f'{match[0].day}. {match[0].month}.,'

    if match[3] == TEAMS_FULLNAMES[team]:
        result += f'{get_abbr_team_name(match[4])},"{match[-1]}"'
    elif match[4] == TEAMS_FULLNAMES[team]:
        result += f'{get_abbr_team_name(match[3])},'
        score_split = match[-1].split(':')

        home_score = score_split[0]
        away_score = score_split[1]
        p = ''
        so = ''

        if not away_score.isnumeric():
            if away_score[-1] == 'p':
                p = 'p'
                away_score = int(away_score[:-1])
            elif away_score[-1] == 'n':
                so = 'sn'
                away_score = int(away_score[:-2])
        else:
            away_score = int(away_score)

        result += f'"{away_score}:{home_score}{p}{so}"'

    return result + '\n'


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


def write_table_to_file(table, filename: str):
    """
    Writes contents of given table to file.
    :param table: HTML table with data
    :param filename: name of the file
    :return: nothing
    """
    with open(filename, 'w', encoding='utf-8') as f:
        for tr in table.find_all('tr'):
            s = read_cells_in_row(tr)
            f.write(s)


def write_best_of_tables_to_file(tables, filename: str):
    """
    Writes contents of given list of tables to one "best-of" file.
    :param tables: list of tables with best-of stats
    :param filename: name of the file
    :return: nothing
    """
    with open(filename, 'w', encoding='utf-8') as f:
        for i in range(len(tables)):
            counter = 0
            for tr in tables[i].find_all('tr'):
                s = read_cells_in_row(tr)
                counter += 1
                f.write(s)

            for j in range(counter, 5):
                f.write(',,,\n')


def read_cells_in_row(row):
    """
    Reads all cells in a given row of some table.
    :param row: row of HTML table (<c><tr></c>)
    :return: string with row data
    """
    s = ''
    for td in row.find_all('td'):
        if ',' in td.text.strip():
            s = s + '"' + td.text.strip() + '"'
        else:
            s += td.text.strip()
        s += ','

    s = s[:-1] + '\n'

    return s


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
    # checks if this year's csv directory exists, if not, creates it
    if not os.path.exists(f'csv_{SEASON_FIRST_YEAR}{SEASON_SECOND_YEAR}'):
        os.makedirs(f'csv_{SEASON_FIRST_YEAR}{SEASON_SECOND_YEAR}')

    read_league_table()

    for team in TEAMS_DICT.keys():
        print('-------------------------------')
        read_team_players_stats(team)
        read_team_goalies_stats(team)
        read_team_bestof_stats(team)
        read_team_matches(team)


TABLE = r'https://www.ceskyflorbal.cz/superliga-muzi/tabulka'
BASE_URL = r'https://www.ceskyflorbal.cz/druzstvo/'
TEAMS_DICT = {'VIT': '27231', 'MB': '27929', 'TAT': '26841', 'BOH': '28310', 'CHO': '26151', 'OST': '26682',
              'SPA': '26345', 'BA': '28078', 'LIB': '26709', 'HAT': '27660', 'CLP': '28266', 'PAR': '28194',
              'OTR': '26086', 'SKV': '26475'}
TEAMS_FULLNAMES = {'VIT': '1. SC TEMPISH Vítkovice', 'MB': 'Předvýběr.CZ Florbal MB',
                   'TAT': 'Tatran Teka Střešovice', 'BOH': 'FbŠ Bohemians', 'CHO': 'FAT PIPE FLORBAL CHODOV',
                   'OST': 'FBC ČPP OSTRAVA', 'SPA': 'ACEMA Sparta Praha', 'BA': 'BLACK ANGELS', 'LIB': 'FBC Liberec',
                   'HAT': 'FBŠ Hummel Hattrick Brno', 'CLP': 'FBC 4CLEAN Česká Lípa', 'PAR': 'SOKOLI Pardubice',
                   'OTR': 'Hu-Fa PANTHERS OTROKOVICE', 'SKV': 'TJ Sokol Královské Vinohrady'}
SEASON_FIRST_YEAR = 20
SEASON_SECOND_YEAR = 21

if __name__ == '__main__':
    main()
