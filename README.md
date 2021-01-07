# Automatic commentary preparation maker
Designed to scrape official web of Czech floorball to derive statistics of
the league and of all 14 teams.

## Script
The script runs for approx. 5 minutes before creating `.csv` files with scraped
data. The data are divided into small files for easier importing to Excel.

## `.csv` files
The files are named according to their content, so that they can be easily
identified. For example, the file `tabulka.csv` contains the table of the
league, whereas the file `vitkovice_asistence.csv` contains information about
best players in assists from Vítkovice.

## Preparations
The Excel file with the preparations themselves is almost automatic. When
selecting players to the line-up of some team, all information about individual
players are loaded from data sheets, which had loaded data from `.csv` files
when the workbook was being opened.