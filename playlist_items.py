from spotipy.oauth2 import SpotifyClientCredentials
import spotipy
from pprint import pprint
import cred

client_credentials_manager = SpotifyClientCredentials(client_id=cred.SPOTIPY_CLIENT_ID, client_secret=cred.SPOTIPY_CLIENT_SECRET)
sp = spotipy.Spotify(client_credentials_manager=client_credentials_manager)

pl_id = 'spotify:playlist:658hRQOsvhq2J8Yog607f1'


response = sp.playlist_items(pl_id,
                                fields='items.track.name, items.track.artist',
                                additional_types=['track'])
pprint(response)