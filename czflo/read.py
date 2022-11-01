import re
import requests
from bs4 import BeautifulSoup


def read_league_table_old(tbl: str):
    """
    !! WARNING !! This function is deprecated since October 2022 when
    Český florbal released a new website.

    Reads league team stats.
    :param tbl: URL with table location
    :return: nothing
    """
    from czflo.write import write_table_to_file_old

    url = tbl
    page = requests.get(url)

    # if opening the page was OK
    if page.status_code == 200:
        print("League table page opened successfully...")

        soup = BeautifulSoup(page.text, 'html.parser')

        table = soup.find('tbody', id=re.compile('^datablock-TeamStatsDataGrid_'))

        write_table_to_file_old(table, f'aktualni/csv/league_table.csv')
    else:
        print(f'ERROR: Unsuccessful loading of league table page!')
