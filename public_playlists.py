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


def shared_artists(uri1, uri2):
    def all_artits_in_playlist(playlist_uri):
        all_artists = []
        for track in get_playlist_tracks(playlist_uri):
            for artist in track.artists:
                all_artists.append(artist)
        return all_artists

    u1_artists = all_artits_in_playlist(uri1)
    u2_artists = all_artits_in_playlist(uri2)

    u1_dic = {artist: u1_artists.count(artist) for artist in set(u1_artists)}
    u2_dic = {artist: u2_artists.count(artist) for artist in set(u2_artists)}

    intersects = set(u1_artists).intersection(set(u2_artists))

    for artist in intersects:
        print(f'{artist} - u1: {u1_dic[artist]} - u2: {u2_dic[artist]}')

    print(f'Here are all the artists you both listen to:')
    print(f'ARTIST | TOTAL TRACKS | P1 TRACKS | P2 TRACKS')


def shared_songs(uri1, uri2):
    u1_songs = get_all_tracks_from_person(uri1)
    u2_songs = get_all_tracks_from_person(uri2)

    intersects = set(u1_songs).intersection(set(u2_songs))
    print(intersects)
    print(f'Out of the {len(u1_songs) + len(u2_songs)} songs in both of your public playlists, you share {len(intersects)} in common.')
    

def get_all_tracks_from_person(uri):
    playlists = get_public_playlists(uri)
    all_playlist_objects = [get_playlist_tracks(playlist.uri) for playlist in playlists]
    all_tracks = []
    for playlist in all_playlist_objects:
        for track in playlist:
            all_tracks.append(track.name)
    return all_tracks


def get_all_artists_from_person(uri):
    playlists = get_public_playlists(uri)
    all_playlist_objects = [get_playlist_tracks(playlist.uri) for playlist in playlists]
    all_artists = []
    for playlist in all_playlist_objects:
        for track in playlist:
            for artist in track.artists:
                all_artists.append(artist)
    return all_artists

def get_artist_dic(uri):
    artists = get_all_artists_from_person(uri)
    return {artist: artists.count(artist) for artist in artists}


def shared_artists_ranked(uri1, uri2):
    p1_dic = get_artist_dic(uri1)
    p2_dic = get_artist_dic(uri2)

    intersect = set(p1_dic).intersection(set(p2_dic))

    print(f'Out of the {len(p1_dic) + len(p2_dic)} artists you listen to, you share {len(intersect)} in common.')
    print('ARTIST | TOTAL | P1 AMOUNT | P2 AMOUNT')
    for artist in intersect:
        p1_amount = p1_dic[artist]
        p2_amount = p2_dic[artist]
        print(f'{artist} | {p1_amount + p2_amount} | {p1_amount} | {p2_amount}')
