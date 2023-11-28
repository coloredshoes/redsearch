import click
import pandas as pd
import requests
import yaml
from bs4 import BeautifulSoup
from unidecode import unidecode

DEF_OUTPUT_FILE = "resources/channels.yaml"

def get_channel_html(url):
    """
    Get the html of a channel.
    """
    response = requests.get(url)
    return BeautifulSoup(response.text)

def get_description(html):
    """
    Get the description of a channel.
    """
    description = html.find("meta", attrs={"name": "description"})
    return unidecode(description["content"].replace("\n", " "))


def get_name(html):
    """
    Get the name of a channel.
    """
    return html.find("meta", attrs={"itemprop": "name"})["content"]


def get_channel_id(html):
    """
    Get the channel_id of a channel.
    """
    return html.find("meta", attrs={"itemprop": "identifier"})["content"]


@click.command()
@click.argument("file", type=click.File("r"))
@click.argument("output", type=click.File("w"), default=DEF_OUTPUT_FILE)
def get_channel_information(file, output):
    channels = []
    for line in file:
        url = line.strip()
        click.echo(f"Getting information for {url}")
        html = get_channel_html(url)
        name = get_name(html)
        description = get_description(html)
        channel_id = get_channel_id(html)
        channels.append({"name": name, "description": description, "id": channel_id, "url": url})
        click.echo(f"Logging output {url}:")
        click.echo(f"    name: {name}")
        click.echo(f"    description: {description}")
        click.echo(f"    channel_id: {channel_id}")

    channels = [
        {
            "id": k,
            "name": item["name"],
            "url": item["url"],
            "description": item["description"],
            "channel_id": item["id"]
        }
        for k, item in enumerate(sorted(channels, key=lambda x: x["name"]))
    ]
    yaml.dump(channels, output)
    pd.DataFrame(channels).set_index("id").to_excel("resources/channels.xlsx")
