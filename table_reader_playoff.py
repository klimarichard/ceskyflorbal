import re
import os
from bs4 import BeautifulSoup
from selenium import webdriver
from time import sleep


def read_playoff_table(driver):
    """
    Reads league play-off team stats.
    :param driver: selenium webdriver
    :return: nothing
    """
    driver.get(TABLE)
    driver.find_element_by_xpath('/html/body/div[3]/div/div[3]/div/div/div/div/div/div/div/div[3]/div/div/div/div/div[1]/div[2]/form/span[3]/select/option[2]').click()

    sleep(7.5)

    page = driver.page_source

    print("League play-off table page opened...")

    soup = BeautifulSoup(page, 'html.parser')

    table = soup.find('tbody', id=re.compile('^datablock-TeamStatsDataGrid_'))

    with open(f'csv_{SEASON_FIRST_YEAR}{SEASON_SECOND_YEAR}/tabulka_playoff.csv', 'w', encoding='utf-8') as f:
        for tr in table.find_all('tr'):
            s = ''
            for td in tr.find_all('td'):
                s += td.text.strip()
                s += ','

            s = s[:-1] + '\n'
            f.write(s)


def read_team_players_playoff_stats(team: str, driver):
    """
    Reads play-off stats of all players from given team.
    :param team: team abbreviated name
    :param driver: selenium webdriver
    :return: nothing
    """
    driver.get(BASE_URL + TEAMS_DICT[team] + '/statistiky/hraci')
    driver.find_element_by_xpath(
        '/html/body/div[3]/div/div[4]/div/div/div/div[2]/div/div/div/div[2]/div/div/div/div[2]/div/div/div/div[1]/div/form/div/select/option[2]').click()

    sleep(7.5)

    page = driver.page_source

    print(f"Players play-off stats table page for {team.upper()} opened...")

    soup = BeautifulSoup(page, 'html.parser')

    table = soup.find('tbody', id=re.compile('^datablock-PlayerStatsDataGrid'))

    write_table_to_file(table, f'csv_{SEASON_FIRST_YEAR}{SEASON_SECOND_YEAR}/{team}_players_playoff.csv')


def read_team_goalies_playoff_stats(team: str, driver):
    """
    Reads play-off stats of all goalies from given team.
    :param team: team abbreviated name
    :param driver: selenium webdriver
    :return: nothing
    """
    driver.get(BASE_URL + TEAMS_DICT[team] + '/statistiky/brankari')
    driver.find_element_by_xpath(
        '/html/body/div[3]/div/div[4]/div/div/div/div[2]/div/div/div/div[2]/div/div/div/div[2]/div/div/div/div[1]/div/form/div/select/option[2]').click()

    sleep(7.5)

    page = driver.page_source

    print(f"Goalies play-off stats table page for {team.upper()} opened...")

    soup = BeautifulSoup(page, 'html.parser')

    table = soup.find('tbody', id=re.compile('^datablock-GoalieStatsDataGrid'))

    write_table_to_file(table, f'csv_{SEASON_FIRST_YEAR}{SEASON_SECOND_YEAR}/{team}_goalies_playoff.csv')


def read_team_bestof_playoff_stats(team, driver):
    """
    Reads best-of play-off statistics of given team.
    :param team: team abbreviated name
    :param driver: selenium webdriver
    :return: nothing
    """
    driver.get(BASE_URL + TEAMS_DICT[team] + '/statistiky/')
    driver.find_element_by_xpath(
        '/html/body/div[3]/div/div[4]/div/div/div/div[2]/div/div/div/div[2]/div/div/div/div[2]/div/div/div/div[1]/div/form/div/select/option[2]').click()

    sleep(7.5)

    page = driver.page_source

    print(f"Best-of play-off stats table page for {team.upper()} opened...")

    soup = BeautifulSoup(page, 'html.parser')

    tables = soup.findAll('table', {'class': 'statTable'})

    write_best_of_tables_to_file(tables, f'csv_{SEASON_FIRST_YEAR}{SEASON_SECOND_YEAR}/{team}_bestof_playoff.csv')


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


def extract_playoff_stats():
    """
    Performs all stats extraction for play-off using selenium.
    :return: nothing
    """
    driver = webdriver.Firefox()
    print('-------------------------------')
    print('PLAY-OFF STATISTICS:')

    read_playoff_table(driver)

    for team in TEAMS_PLAYOFF_DICT.keys():
        print('-------------------------------')
        read_team_players_playoff_stats(team, driver)
        read_team_goalies_playoff_stats(team, driver)
        read_team_bestof_playoff_stats(team, driver)

    driver.close()


def main():
    """
    Main function of the script.
    :return: nothing
    """
    # checks if this year's csv directory exists, if not, creates it
    if not os.path.exists(f'csv_{SEASON_FIRST_YEAR}{SEASON_SECOND_YEAR}'):
        os.makedirs(f'csv_{SEASON_FIRST_YEAR}{SEASON_SECOND_YEAR}')

    extract_playoff_stats()


TABLE = r'https://www.ceskyflorbal.cz/superliga-muzi/tabulka'
BASE_URL = r'https://www.ceskyflorbal.cz/druzstvo/'
TEAMS_DICT = {'VIT': '27231', 'MB': '27929', 'TAT': '26841', 'BOH': '28310', 'CHO': '26151', 'OST': '26682',
              'SPA': '26345', 'BA': '28078', 'LIB': '26709', 'HAT': '27660', 'CLP': '28266', 'PAR': '28194',
              'OTR': '26086', 'SKV': '26475'}
TEAMS_PLAYOFF_DICT = {'VIT': '27231', 'MB': '27929', 'TAT': '26841', 'BOH': '28310', 'CHO': '26151', 'OST': '26682',
                      'SPA': '26345', 'BA': '28078'}
TEAMS_FULLNAMES = {'VIT': '1. SC TEMPISH Vítkovice', 'MB': 'Předvýběr.CZ Florbal MB',
                   'TAT': 'Tatran Teka Střešovice', 'BOH': 'FbŠ Bohemians', 'CHO': 'FAT PIPE FLORBAL CHODOV',
                   'OST': 'FBC ČPP OSTRAVA', 'SPA': 'ACEMA Sparta Praha', 'BA': 'BLACK ANGELS', 'LIB': 'FBC Liberec',
                   'HAT': 'FBŠ Hummel Hattrick Brno', 'CLP': 'FBC 4CLEAN Česká Lípa', 'PAR': 'SOKOLI Pardubice',
                   'OTR': 'Hu-Fa PANTHERS OTROKOVICE', 'SKV': 'TJ Sokol Královské Vinohrady'}
SEASON_FIRST_YEAR = 20
SEASON_SECOND_YEAR = 21

if __name__ == '__main__':
    main()
