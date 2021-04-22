import pathlib
from urllib.request import urlopen

import click
import pandas as pd

from cscrawler.parser.homepage import parse_html, debug_df, update_data_file


@click.group()
@click.option('--debug/--no-debug', default=False)
@click.option('--output-file', type=click.STRING, help='Output data file to append to.')
@click.pass_context
def cli(ctx, debug, output_file):
    """Crawler for covid19.saglik.gov.tr.

    OUTPUT_FILE is the path to an output CSV file for the crawled provincial case numbers.
    No-op when omitted.
    """

    ctx.ensure_object(dict)
    ctx.obj['DEBUG'] = debug
    ctx.obj['OUTPUT_FILE'] = output_file


def read_file(html_file):
    """Read file.
    
    Returns contents of file as text.
    """

    f = pathlib.Path(html_file)

    if not f.exists():
        click.echo(f"{f} does not exist.")

    return f.read_text()


@cli.command("parse_file")
@click.argument('html_file', type=click.STRING, required=True)
@click.pass_context
def parse_file(ctx, html_file):
    """Parse the given HTML file representation of the covid19.saglik.gov.tr website.

    HTML_FILE is the path to the file.
    """

    html = read_file(html_file)
    df = parse_html(html)
    debug_df(df)

    if ctx.obj['OUTPUT_FILE']:
        update_data_file(ctx.obj['OUTPUT_FILE'], df)


@cli.command("parse_files")
@click.argument('html_dir', type=click.STRING, required=True)
@click.pass_context
def parse_files(ctx, html_dir):
    """Parse the given directory of HTML files, where each represents the home page of
    covid19.saglik.gov.tr from different days.

    HTML_DIR is the directory of HTML files.
    """

    html_dir_path = pathlib.Path(html_dir)

    dfs = []
    for f in html_dir_path.glob('*.html'):
        dfs.append(parse_html(read_file(f)))
    df = pd.concat(dfs, ignore_index=True)
    debug_df(df)

    if ctx.obj['OUTPUT_FILE']:
        update_data_file(ctx.obj['OUTPUT_FILE'], df)


@cli.command("parse_url")
@click.pass_context
def parse_url(ctx, url='https://covid19.saglik.gov.tr'):
    """Parse the covid19.saglik.gov.tr website.
    """

    page = urlopen(url)
    html_bytes = page.read()
    html = html_bytes.decode("utf-8")
    df = parse_html(html)
    debug_df(df)
    
    if ctx.obj['OUTPUT_FILE']:
        update_data_file(ctx.obj['OUTPUT_FILE'], df)   
