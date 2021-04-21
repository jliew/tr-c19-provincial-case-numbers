import locale
import re

import click
import pandas as pd
from bs4 import BeautifulSoup
from dateparser.date import DateDataParser


def debug_df(df):
    """Print DataFrame info."""

    click.echo(df)
    click.echo(df.info())
    click.echo(df.groupby(['original_week_period', 'original_date_text', 'date']).count())


def find_data(soup):
    """Parse g tags containing data attributes, put data into DataFrame.
    """

    data_results = soup.find_all(lambda tag: tag.has_attr('data-adi') and tag.has_attr('data-detay'))
    return pd.DataFrame([ child.attrs for child in data_results ])


def find_current_date(soup):
    """Parse tag containing current date.

    Return string containing current date.
    """

    for r in soup.find_all(lambda tag: tag.name == 'h3' and tag.has_attr('class')):
        if 'full_date' in r['class']:
            return r.string.strip()

    raise Exception("Couldn't find current date in HTML.")


def find_week_date(soup):
    """Parse tag containing week dates.

    Return string containing week date.
    """

    for r in soup.find_all(lambda tag: tag.name == 'h2' and tag.string is not None \
            and tag.string.strip() == 'İllere Göre Haftalık Vaka Sayısı (100 binde)'):
        for sibling in r.find_next_siblings("p"):
            text = sibling.get_text().strip()
            if text != '':
                return text

        for sibling in r.find_next_siblings("h3"):
            text = sibling.get_text().strip()
            if text != '':
                return text

    raise Exception("Couldn't find week dates in HTML.")


def parse_html(html):
    """Parse data from string containing HTML.

    Returns a DataFrame.
    """

    soup = BeautifulSoup(html, 'html.parser')
    df = find_data(soup)

    # append original date column
    original_week_period = find_week_date(soup)
    df['original_week_period'] = original_week_period

    # extract date value from text
    date_search = re.search('(\d+\s+\w+\s+\d{2,4})$', original_week_period, re.IGNORECASE)
    if date_search:
        original_date_text = date_search.group(1)
        df['original_date_text'] = original_date_text
    else:
        raise Exception(f"Couldn't extract date from date text {original_week_period}.")

    # parse date
    ddp = DateDataParser(languages=['tr'], settings={'DATE_ORDER': 'DMY'})
    df['date'] = ddp.get_date_data(original_date_text).date_obj

    # parse numeric 'vaka sayısı' figure using TR locale
    locale.setlocale(locale.LC_NUMERIC, 'tr_TR')
    df['data-detay'] = df['data-detay'].apply(locale.atof)

    # remove dash from column names
    df = df.rename(columns={
        'data-adi': 'data_adi',
        'data-detay': 'data_detay'
    })
    
    return df[['data_adi', 'data_detay', 'original_week_period', 'original_date_text', 'date']]
