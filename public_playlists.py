
   
# Gets all the public playlists for the given
# user. Uses Client Credentials flow
#

import sys
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
import cred

client_credentials_manager = SpotifyClientCredentials(client_id=cred.SPOTIPY_CLIENT_ID, client_secret=cred.SPOTIPY_CLIENT_SECRET)
sp = spotipy.Spotify(client_credentials_manager=client_credentials_manager)


def get_public_playlists(user: str):
    playlists = sp.user_playlists(user)
    


user = 'chelseasoemitro'

playlists = sp.user_playlists(user)

while playlists:
    for i, playlist in enumerate(playlists['items']):
        print(
            "%4d %s %s" %
            (i +
             1 +
             playlists['offset'],
             playlist['uri'],
             playlist['name']))
    if playlists['next']:
        playlists = sp.next(playlists)
    else:
        playlists = None