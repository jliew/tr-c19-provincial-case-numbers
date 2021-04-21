import pathlib
from urllib.request import urlopen

import click
import pandas as pd

from cscrawler.parser.homepage import parse_html, debug_df


@click.group()
@click.option('--debug/--no-debug', default=False)
@click.pass_context
def cli(ctx, debug):
    ctx.ensure_object(dict)
    ctx.obj['DEBUG'] = debug


def read_file(html_file):
    """Read file.
    
    Returns contents of file as text.
    """

    f = pathlib.Path(html_file)

    if not f.exists():
        click.echo(f"{f} does not exist.")

    return f.read_text()


@cli.command("parse_file")
@click.option('--output-csv', is_flag=True, help='Output data as CSV to stdout.')
@click.argument('html_file', type=click.STRING, required=True)
@click.pass_context
def parse_file(ctx, html_file, output_csv):
    html = read_file(html_file)
    df = parse_html(html)
    
    if output_csv:
        click.echo(df.to_csv(None, index=False))
    else:
        debug_df(df)


@cli.command("parse_files")
@click.argument('html_dir', type=click.STRING, required=True)
@click.option('--output-csv', is_flag=True, help='Output data as CSV to stdout.')
@click.pass_context
def parse_files(ctx, html_dir, output_csv):
    html_dir_path = pathlib.Path(html_dir)

    dfs = []
    for f in html_dir_path.glob('*.html'):
        dfs.append(parse_html(read_file(f)))
    df = pd.concat(dfs, ignore_index=True)

    if output_csv:
        click.echo(df.to_csv(None, index=False))
    else:
        debug_df(df)


@cli.command("parse_url")
@click.option('--output-csv', is_flag=True, help='Output data as CSV to stdout.')
@click.pass_context
def parse_url(ctx, output_csv, url='https://covid19.saglik.gov.tr',):
    page = urlopen(url)
    html_bytes = page.read()
    html = html_bytes.decode("utf-8")
    df = parse_html(html)
    
    if output_csv:
        click.echo(df.to_csv(None, index=False))
    else:
        debug_df(df)
