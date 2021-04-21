# Turkey COVID-19 Provincial Case Numbers (per 100k)

Now that the Turkish Ministry of Health publishes province-level case numbers, this project makes that
data available as a CSV file.

## Manual usage

Set up local virtual env using [poetry](https://python-poetry.org/docs/):

`poetry install`

Parse the website and output some stats to stdout:

`poetry run cscrawler parse_url`

Parse the website and output the data in CSV format to stdout:

`poetry run cscrawler parse_url --output-csv`
