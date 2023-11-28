from googleapiclient.discovery import build
from youtube_transcript_api import YouTubeTranscriptApi


def get_client(api_key):
    return build("youtube", "v3", developerKey=api_key)


def get_uploads_playlist_id(client, channel_id):
    """
    Get the uploads playlist_id from a channel using the YouTube Data API.
    """
    request = client.channels().list(part="contentDetails", id=channel_id)
    response = request.execute()
    return response["items"][0]["contentDetails"]["relatedPlaylists"]["uploads"]


def iterate_on_videos(client, channel_id):
    """
    Get the videos from a channel using the YouTube Data API.
    """
    playlist_id = get_uploads_playlist_id(client, channel_id)
    next_page_token = None

    while True:
        request = client.playlistItems().list(
            part="contentDetails",
            playlistId=playlist_id,
            maxResults=50,
            pageToken=next_page_token,
        )
        response = request.execute()
        yield from [item["contentDetails"]["videoId"] for item in response["items"]]
        next_page_token = response.get("nextPageToken")
        if not next_page_token:
            break


def get_video_transcription(video_id, language="pt"):
    """
    Get the transcription of a video.
    """
    transcript = YouTubeTranscriptApi.get_transcript(video_id, languages=[language])
    return transcript
