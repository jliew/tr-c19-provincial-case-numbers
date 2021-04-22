# Turkey COVID-19 Provincial Case Numbers (per 100k)

Now that the Turkish Ministry of Health publishes province-level case numbers, this project makes that
data available as a CSV file and through a Tableau Web Data Connector.

## Tableau WDC

Connect from Tableau Desktop by using this Web Data Connector URL:

`https://jliew.github.io/tr-c19-provincial-case-numbers/tableau_wdc/turkey_case_numbers_by_province.html`

## Manual usage

Set up local virtual env using [poetry](https://python-poetry.org/docs/):

`poetry install`

Parse the website and output some stats to stdout:

`poetry run cscrawler parse_url`

Parse the website and update the specified output CSV file:

`poetry run cscrawler --output-file data/vaka_sayısı.csv parse_url`
