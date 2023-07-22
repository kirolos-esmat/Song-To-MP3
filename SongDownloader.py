import os
import re
import spotipy
from pytube import YouTube
from spotipy.oauth2 import SpotifyClientCredentials
from googleapiclient.discovery import build

# Set your Spotify API credentials
SPOTIPY_CLIENT_ID = "YOUR_SPOTIFY_CLIENT_ID"
SPOTIPY_CLIENT_SECRET = "YOUR_SPOTIFY_CLIENT_SECRET"

# Set your YouTube API key
YOUTUBE_API_KEY = "YOUR_YOUTUBE_API_KEY"

# Set your destination folder for download
Destination = 'YOUR_DESTINATION' or '.'

# Initialize the Spotify client
spotify = spotipy.Spotify(client_credentials_manager=SpotifyClientCredentials(SPOTIPY_CLIENT_ID, SPOTIPY_CLIENT_SECRET))

# ---------------------------------------------------------------------------------------------------------------------- #

def get_spotify_song_link(artist, track):
    # Search for the track on Spotify
    results = spotify.search(q=f"artist:{artist} track:{track}", type="track", limit=1)

    # Extract and return the Spotify song link
    if results and results["tracks"]["items"]:
        song_link = results["tracks"]["items"][0]["external_urls"]["spotify"]
        return song_link
    else:
        return None

def get_spotify_playlist_tracks(playlist_url):
    # Extract playlist ID from the Spotify playlist URL
    playlist_id_match = re.search(r"/playlist/(\w+)", playlist_url)
    if playlist_id_match:
        playlist_id = playlist_id_match.group(1)
    else:
        print("Invalid Spotify playlist link.")
        exit()

    # Get tracks from the playlist
    playlist_tracks = []
    offset = 0
    limit = 100
    while True:
        results = spotify.playlist_tracks(playlist_id, fields="items(track(name,artists(name)))", limit=limit, offset=offset)
        if not results["items"]:
            break

        for item in results["items"]:
            track_info = item["track"]
            artist = track_info["artists"][0]["name"]
            track = track_info["name"]
            playlist_tracks.append((artist, track))

        offset += limit

    return playlist_tracks

def get_youtube_video_id(query):
    # Initialize the YouTube Data API client
    youtube = build("youtube", "v3", developerKey=YOUTUBE_API_KEY)

    # Search for the video on YouTube
    search_response = youtube.search().list(q=query, part="id", maxResults=1, type="video").execute()

    # Extract and return the YouTube video ID
    if "items" in search_response:
        for item in search_response["items"]:
            return item["id"]["videoId"]
    return None

def get_youtube_playlist_video_ids(playlist_url):
    # Extract playlist ID from the YouTube playlist URL
    playlist_id_match = re.search(r"list=(\w+)", playlist_url)
    if playlist_id_match:
        playlist_id = playlist_id_match.group(1)
    else:
        print("Invalid YouTube playlist link.")
        exit()

    # Initialize the YouTube Data API client
    youtube = build("youtube", "v3", developerKey=YOUTUBE_API_KEY)

    # Get videos from the playlist
    playlist_response = youtube.playlistItems().list(
        playlistId=playlist_id,
        part="snippet",
        maxResults=50  # Increase if needed
    ).execute()

    # Extract video IDs from the playlist
    video_ids = []
    for item in playlist_response["items"]:
        video_ids.append(item["snippet"]["resourceId"]["videoId"])

    return video_ids

def download_ytvid_as_mp3(yt_link):
    yt = YouTube(yt_link)
    video = yt.streams.filter(only_audio=True).first()
    out_file = video.download(output_path=Destination)
    base, ext = os.path.splitext(out_file)
    new_file = base + '.mp3'
    os.rename(out_file, new_file)
    print(yt.title + " has been successfully downloaded.\n")

# ---------------------------------------------------------------------------------------------------------------------- #

# The main function
if __name__ == "__main__":
    spotify_or_youtube = input("Enter 's' for Spotify song link, 'p' for Spotify playlist link, or 'y' for YouTube song/playlist link: ")

    if spotify_or_youtube.lower() == "s":
        spotify_url = input("Enter the Spotify song link: ")

        # Extract track ID from the Spotify URL
        track_id_match = re.search(r"/track/(\w+)", spotify_url)
        if track_id_match:
            track_id = track_id_match.group(1)
        else:
            print("Invalid Spotify song link.")
            exit()

        # Get track information
        track_info = spotify.track(track_id)
        artist = track_info["artists"][0]["name"]
        track = track_info["name"]

        # Get the Spotify song link
        spotify_link = get_spotify_song_link(artist, track)

        if spotify_link:
            print("Spotify song link:", spotify_link)
        else:
            print("Song not found on Spotify.")

        # Get the YouTube video ID
        youtube_video_id = get_youtube_video_id(f"{artist} {track}")

        if youtube_video_id:
            youtube_link = f"https://www.youtube.com/watch?v={youtube_video_id}"
            print("YouTube video link:", youtube_link)
        else:
            print("YouTube video not found.")

        # Download the video into mp3 format
        download_ytvid_as_mp3(youtube_link)

    elif spotify_or_youtube.lower() == "p":
        spotify_url = input("Enter the Spotify playlist link: ")

        # Get tracks from the playlist
        playlist_tracks = get_spotify_playlist_tracks(spotify_url)
        for artist, track in playlist_tracks:
            # Get the Spotify song link
            spotify_link = get_spotify_song_link(artist, track)

            if spotify_link:
                print(f"Spotify song link for {track} by {artist}: {spotify_link}")

                # Get the YouTube video ID
                youtube_video_id = get_youtube_video_id(f"{artist} {track}")

                if youtube_video_id:
                    youtube_link = f"https://www.youtube.com/watch?v={youtube_video_id}"
                    print("YouTube video link:", youtube_link)

                    # Download the video into mp3 format
                    download_ytvid_as_mp3(youtube_link)
                else:
                    print(f"YouTube video not found for {track} by {artist}.")
            else:
                print(f"Song not found on Spotify: {track} by {artist}.")

    elif spotify_or_youtube.lower() == "y":
        youtube_link = input("Enter the YouTube song/playlist link: ")

        if "list=" in youtube_link:
            # Download from playlist
            video_ids = get_youtube_playlist_video_ids(youtube_link)
            for video_id in video_ids:
                youtube_link = f"https://www.youtube.com/watch?v={video_id}"
                download_ytvid_as_mp3(youtube_link)
        else:
            # Download single song
            youtube_video_id = get_youtube_video_id(youtube_link)

            if youtube_video_id:
                youtube_link = f"https://www.youtube.com/watch?v={youtube_video_id}"
                download_ytvid_as_mp3(youtube_link)
            else:
                print("YouTube video not found.")
    else:
        print("Invalid input. Please enter 's', 'p', or 'y'.")
