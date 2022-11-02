import bs4


def write_table_to_file_old(table: bs4.BeautifulSoup, file_name: str):
    """
    !! WARNING !! This function is deprecated since October 2022 when
    Český florbal released a new website.

    Writes a parsed table to a given CSV file.
    :param table: a BeautifulSoup element with the table body
    :param file_name: path to target CSV file
    :return: nothing
    """
    with open(file_name, 'w', encoding='utf-8') as f:
        for tr in table.find_all('tr'):
            s = ''
            for td in tr.find_all('td'):
                s += td.text.strip()
                s += ','

            s = s[:-1] + '\n'
            f.write(s)
