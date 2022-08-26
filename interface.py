import cred
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials


client_credentials_manger = SpotifyClientCredentials(client_id=cred.SPOTIFY_CLIENT_ID, client_secret=cred.SPOTIFY_CLIENT_SECRET)

sp = spotipy.Spotify(client_credentials_manager=client_credentials_manger)


"""
Input: two users

Output:
    - % sameness
    - common genres
    - common songs (ranked by occurances)
    - common artists (ranked by occurances)
"""


def get_public_playlists(user: str) -> list:
    """Returns a user's public playlists."""
    playlists = sp.user_playlists(user)
    
    playlist_uri_so_far = []
    while playlists:
        for playlist in playlists['items']:
            playlist_uri_so_far.append(playlist['uri'])
        if playlists['next']:  # if first response overflows
            playlists = sp.next(playlists)
        else:
            playlists = None
    
    return playlist_uri_so_far


def get_single_playlist_tracks(user: str) -> list:
    """Returns a list of (SONG_NAME, [ARTIST]) given a URI."""
    tracks_paginated = []
    offest = 0
    while True:
    