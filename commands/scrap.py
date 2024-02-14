import click
import yaml
from scrap.youtube import get_client, iterate_on_videos, get_video_transcription
from unidecode import unidecode
import os
from pathlib import Path

with open("resources/secrets.yaml") as f:
    data = yaml.load(f, yaml.BaseLoader)
    API_KEY = data["youtube"]["api_key"]

print(__file__)


def iterate_channels(file_path):
    with open(file_path) as f:
        data = yaml.load(f, yaml.BaseLoader)
        for channel in data:
            yield channel


def make_channel_slug(channel):
    return unidecode(channel["name"]).lower().replace(" ", "-").replace("/", "-")


def ensure_channel_output_dir(channel):
    channel_slug = make_channel_slug(channel)
    channel_path = f"resources/videos/{channel_slug}"
    os.makedirs(channel_path, exist_ok=True)
    return Path(channel_path)


def get_video_path(video, channel_path):
    return channel_path / f"{video['video_id']}.yaml"


def check_video_exists(video, channel_path):
    video_path = get_video_path(video, channel_path)
    return video_path.exists()


def save_video(video, channel_path):
    video_path = channel_path / f"{video['video_id']}.yaml"
    with open(video_path, "w") as f:
        yaml.dump(video, f)


@click.command()
def clean_files_without_transcriptions():
    """Clean files without transcriptions"""
    for channel in os.listdir("resources/videos"):
        for video in os.listdir(f"resources/videos/{channel}"):
            video_path = f"resources/videos/{channel}/{video}"
            with open(video_path) as f:
                data = yaml.load(f, yaml.BaseLoader)
                has_transcript = len(data.get("transcriptions", {})) > 0
                if not has_transcript:
                    click.echo(f"Removing {video_path}: no transcriptions found.")
                    os.remove(video_path)
                else:
                    click.echo(f"Keeping {video_path}. Found transcriptions:")


@click.command()
@click.argument("path", type=click.Path(exists=True))
def scrap(path):
    """Scrap the data from YouTube"""

    client = get_client(API_KEY)
    for channel in iterate_channels(path):
        try:
            print("Scraping {name}".format(**channel))
            channel_path = ensure_channel_output_dir(channel)
            for video in iterate_on_videos(client, channel["channel_id"]):
                print("\tScraping {title}".format(**video))
                if check_video_exists(video, channel_path):
                    print("\t\tVideo already exists. Skipping...")
                else:
                    transcription = get_video_transcription(video["video_id"])
                    if len(transcription) > 0:
                        video["transcriptions"] = transcription
                        save_video(video, channel_path)
                    else:
                        print("\t\tNo transcription found. Skipping...")
        except Exception as e:
            print(f"Error while scraping {channel['name']}: {e}")
