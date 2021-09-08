# Automatic commentary preparation maker
Designed to scrape official web of Czech floorball to derive statistics of
the league and of all 14 teams.

## Script
The script runs for approx. 50 seconds and creates `.csv` files with scraped
data. The data are divided into small files for easier importing to Excel.

## `.csv` files
The files are named according to their content, so that they can be easily
identified. For example, the file `tabulka.csv` contains the table of the
league, whereas the file `VIT_zapasy.csv` contains information about matches
of team Vítkovice.

## Preparations
The Excel file with the preparations themselves is almost automatic. When
selecting players to the line-up of some team, all information about individual
players are loaded from data sheets, which had loaded data from `.csv` files
when the workbook was being opened.\
\
In the overview page of the match, select two teams from dropdown menus at
the top of the page and all information (with the exception of historic matches)
will load onto the page.\
\
The archive of historic matches on page 4 and 6 of the first sheet holds
information about previously found historic matches between some two teams, so
it wouldn't be necessary to look them up the next time these two teams meet
again. The only matches that might not be present in these archives are the ones
played earlier, than the earliest date of the archived list.
