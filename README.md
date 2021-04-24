# Turkey COVID-19 Provincial Case Numbers (per 100k)

Now that the [Turkish Ministry of Health](https://saglik.gov.tr/) publishes [province-level case numbers](https://covid19.saglik.gov.tr/), this project makes that
data available as a CSV file and through a Tableau Web Data Connector.

The [data file itself](https://github.com/jliew/tr-c19-provincial-case-numbers/blob/master/data/vaka_say%C4%B1s%C4%B1.csv) is automatically updated by a crawler which runs once a day.

[![Crawl website](https://github.com/jliew/tr-c19-provincial-case-numbers/actions/workflows/scheduled-github-action.yml/badge.svg)](https://github.com/jliew/tr-c19-provincial-case-numbers/actions/workflows/scheduled-github-action.yml)

See https://jliew.github.io/tr-c19-provincial-case-numbers for a line chart.

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
