from os import name
import sys
from requests.api import get
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
import cred
from dataclasses import dataclass
from typing import List
from pprint import pprint

client_credentials_manager = SpotifyClientCredentials(
    client_id=cred.SPOTIPY_CLIENT_ID, client_secret=cred.SPOTIPY_CLIENT_SECRET)
sp = spotipy.Spotify(client_credentials_manager=client_credentials_manager)


@dataclass
class Person:
    """Class for keeping track of a person's useful Spotify data."""
    name: str
    playlists: list


@dataclass
class Track:
    """Class for a track's useful Spotify data."""
    name: str
    uri: str
    artists: tuple


@dataclass
class Playlist:
    """Class for a playlists' useful information"""
    name: str
    uri: str
    tracks: list


def get_public_playlists(user: str) -> List[Playlist]:
    playlists = sp.user_playlists(user)

    output = []
    while playlists:
        for playlist in playlists['items']:
            output.append(
                Playlist(name=playlist['name'], uri=playlist['uri'], tracks=[])
            )
        if playlists['next']:
            playlists = sp.next(playlists)
        else:
            playlists = None
    return output


def get_playlist_tracks(pl_id: str):
    """
    """
    tracks_paginated = []
    offset = 0
    while True:
        response = sp.playlist_items(pl_id,
                                     offset=offset,
                                     fields='items.track.id, items.track.name, items.track.artists, items.track.uri, total'
                                     )

        if len(response['items']) == 0:
            break

        tracks_paginated.append(response['items'])
        offset = offset + len(response['items'])

    output = []
    for page in tracks_paginated:
        for track in page:
            if track['track'] != None:
                output.append(
                    Track(name=track['track']['name'],
                          artists=get_all_artists_on_track(
                        track['track']['artists']),
                        uri=track['track']['uri'])
                    )
    return output


def get_all_artists_on_track(artists: list) -> list:
    return [artist['name'] for artist in artists]



def compile_data(user_uri) -> Person:
    """Return a Person object from a uri input"""
    
    playlists = []
    for playlist in get_public_playlists(user_uri):
        playlist.tracks = get_playlist_tracks(playlist.uri)
        playlists.append(playlist)

    return Person(
        playlists=playlists,
        name=sp.user(user_uri)['display_name']
    )
