import json
import os

from dotenv import load_dotenv
import requests
import spotipy
import spotipy.util as util
from spotipy.oauth2 import SpotifyClientCredentials
import tweepy

def get_spotify_top_track_month(username: str):
    # Load Spotify keys
    CLIENT_ID     = os.getenv('SPOTIPY_CLIENT_ID')
    CLIENT_SECRET = os.getenv('SPOTIPY_CLIENT_SECRET')
    token = util.prompt_for_user_token(username=username, scope='user-top-read', client_id=CLIENT_ID, client_secret=CLIENT_SECRET, redirect_uri='https://open.spotify.com/collection/playlists')

    sp = spotipy.Spotify(auth=token)
    results = sp.current_user_top_tracks(limit=1, offset=0, time_range='short_term')
    return results['items'][0]


def post_song_twitter(top_track_json):
    # Load Twitter keys
    TWITTER_API_KEY       = os.getenv('TWITTER_API_KEY')
    TWITTER_SECRET_KEY    = os.getenv('TWITTER_SECRET_KEY')
    TWITTER_ACCESS_TOKEN  = os.getenv('TWITTER_ACCESS_TOKEN')
    TWITTER_ACCESS_SECRET = os.getenv('TWITTER_ACCESS_SECRET')

    # Authenticate to Twitter
    auth = tweepy.OAuthHandler(TWITTER_API_KEY, TWITTER_SECRET_KEY)
    auth.set_access_token(TWITTER_ACCESS_TOKEN, TWITTER_ACCESS_SECRET)

    # Create API object
    api = tweepy.API(auth)

    # Tweet!
    song_name = f"This month top track is {top_track_json['name']} by {top_track_json['artists'][0]['name']}\n\n"
    url = f"You can listen to it here: {top_track_json['external_urls']['spotify']}"
    tweet = song_name + url
    api.update_status(tweet)


if __name__ == '__main__':
    # Load environment variables
    load_dotenv()

    top_track = get_spotify_top_track_month('brusiroy')
    post_song_twitter(top_track)