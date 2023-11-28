import click 
import json 
from scrap.youtube import iterate_on_videos, get_client, get_video_transcription

print(__file__)

def iterate_channels(file_path):
    with open(file_path) as f:
        json_data = json.load(f)
        for channel in json_data:
            yield channel["name"], channel["id"]

@click.command()
@click.argument("path", type=click.Path(exists=True))
def scrap(path):
    """Scrap the data from YouTube"""

    for name, channel_id in iterate_channels(path):
        print(f"Scraping {name}, {channel_id}")

    # client = get_client(api_key)
    # for channel_name, channel_id in iterate_channels("channels.json"):
    #     print(f"Scraping {channel_name}")
    #     for video_id in iterate_on_videos(client, channel_id):
    #         print(f"Scraping {video_id}")
    #         transcription = get_video_transcription(video_id)
    #         print(transcription)
    #         break
    #     break
