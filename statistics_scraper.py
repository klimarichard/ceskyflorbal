from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

import pyperclip
import time
import os
import shutil


def read_league_table():
    """
    Reads the table of the league and saves it into a .csv file.
    :return: nothing
    """
    url_link = cursor_to_url_bar()

    if url_link is not None:
        url_link.send_keys(TABLE)
        load_button.click()

        time.sleep(5)

        print('Processing league table...')
        select_table(2)
        copy_to_clipboard()

        table = pyperclip.paste()
        write_league_table_to_file(table)
    else:
        print('ERROR: Unable to access URL link bar.')


def read_team_statistics(team: str, code: str):
    """
    Read all statistics pages of one team.
    :param team: name of the team files
    :param code: team code from CFbU
    :return: nothing
    """
    url_link = cursor_to_url_bar()

    if url_link is not None:
        # write overview page statistics
        url_link.send_keys(Keys.CONTROL, 'a')
        url_link.send_keys(BASE_URL + code + '/statistiky')
        load_button.click()

        time.sleep(5)

        print(f'Processing stats for team {team}...')
        write_overview_statistics(team)

        # write players page statistics
        url_link.send_keys(Keys.CONTROL, 'a')
        url_link.send_keys(BASE_URL + code + '/statistiky/hraci')
        load_button.click()

        time.sleep(5)

        write_players_statistics(team)

        # write goalies page statistics
        url_link.send_keys(Keys.CONTROL, 'a')
        url_link.send_keys(BASE_URL + code + '/statistiky/brankari')
        load_button.click()

        time.sleep(5)

        write_goalies_statistics(team)
    else:
        print('ERROR: Unable to access URL link bar.')


def write_overview_statistics(team):
    """
    Write overview statistic page.
    :param team: name of the team files
    :return: nothing
    """
    dict_names = {13: 'body', 14: 'prumer', 15: 'goly', 16: 'vyhry', 17: 'asistence', 18: 'tm'}
    for i in range(13, 19):
        select_table(i)
        copy_to_clipboard()

        table = pyperclip.paste()

        with open(f'csv_2021/{team}_{dict_names[i]}.csv', 'w', encoding='utf-8', newline='') as f:
            f.write(table)


def write_players_statistics(team):
    """
    Write players' statistic page.
    :param team: name of the team files
    :return: nothing
    """
    select_table(12)
    copy_to_clipboard()

    table = pyperclip.paste()

    with open(f'csv_2021/{team}_players.csv', 'w', encoding='utf-8', newline='') as f:
        f.write(table)


def write_goalies_statistics(team):
    """
    Write goalies' statistic page.
    :param team: name of the team files
    :return: nothing
    """
    select_table(12)
    copy_to_clipboard()

    table = pyperclip.paste()

    with open(f'csv_2021/{team}_goalies.csv', 'w', encoding='utf-8', newline='') as f:
        f.write(table)


def cursor_to_url_bar():
    """
    Returns the URL link bar object from page.
    :return: URL link bar object
    """
    try:
        url_link = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.ID, 'url'))
        )
        return url_link
    except:
        return None


def go_to_url_tab():
    """
    Clicks on Enter URL tab.
    :return: nothing
    """
    try:
        url_tab = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.ID, 'urlTabLink'))
        )

        url_tab.click()

        for i in range(8):
            url_tab.send_keys(Keys.ARROW_DOWN)
    except:
        print('ERROR: Unable to click URL tab.')


def select_table(i: int):
    """
    Select one of the tables available from the page.
    :param i: number of the table
    :return: nothing
    """
    select_box = driver.find_element_by_id('selTabNum')
    select_box.click()

    try:
        option = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.XPATH,
                                            f'/html/body/div[1]/div[3]/div[2]/form/label/span/select/option[{i + 1}]'))
        )
        option.click()
    except:
        print(f'ERROR: Unable to select table no. {i}')


def copy_to_clipboard():
    """
    Clicks the copy to clipboard button.
    :return: nothing
    """
    copy = driver.find_element_by_xpath('/html/body/div[1]/div[3]/div[2]/form/div[2]/button')
    copy.click()


def write_league_table_to_file(source: str):
    """
    Writes the league table to .csv file.
    :param source: source string
    :return: nothing
    """
    with open('csv_2021/tabulka.csv', 'w', encoding='utf-8', newline='') as f:
        f.write(source)


def copy_from_text_area():
    """
    Copy text from text area.
    :return: text from text area
    """
    text_area.send_keys(Keys.CONTROL, 'a')
    copy_to_clipboard()

    return pyperclip.paste()


PATH = r'D:\klima\Documents\Aplikace\geckodriver.exe'
CONVERTER = r'https://www.convertcsv.com/html-table-to-csv.htm'
TABLE = r'https://www.ceskyflorbal.cz/superliga-muzi/tabulka'
BASE_URL = r'https://www.ceskyflorbal.cz/druzstvo/'
TEAMS_DICT = {'vitkovice': '27231', 'boleslav': '27929', 'tatran': '26841', 'bohemians': '28310',
              'chodov': '26151', 'ostrava': '26682', 'sparta': '26345', 'ba': '28078', 'liberec': '26709',
              'hattrick': '27660', 'clipa': '28266', 'pardubice': '28194', 'otrokovice': '26086',
              'skv': '26475'}

driver = webdriver.Firefox(executable_path=PATH)
driver.get(CONVERTER)

go_to_url_tab()
load_button = driver.find_element_by_id('btnUrl')
text_area = driver.find_element_by_id('txta')

read_league_table()

for key in TEAMS_DICT.keys():
    read_team_statistics(key, TEAMS_DICT[key])

driver.quit()

# destination = r'D:\klima\Documents\SKV\pripravy\csv_2021'
# for file in os.listdir('../csv'):
#     shutil.copy(os.path.join('../csv', file), destination)
