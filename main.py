import spotipy
from spotipy.oauth2 import SpotifyOAuth
import cred

scope = 'user-read-recently-played user-follow-read playlist-read-private user-top-read'

sp = spotipy.Spotify(auth_manager=SpotifyOAuth(
    client_id=cred.SPOTIPY_CLIENT_ID,
    client_secret=cred.SPOTIPY_CLIENT_SECRET,
    redirect_uri=cred.SPOTIPY_REDIRECT_URI,
    scope=scope
))

def recently_played():
    results = sp.current_user_recently_played()
    # for idx, item in enumerate(results['items']):
    #     track = item['track']
    #     print(idx, track['artists'][0]['name'], " — ", track['name'])
    print(results)

def current_user_top_artist():
    ranges = ['short_term', 'medium_term', 'long_term']

    for sp_range in ['short_term', 'medium_term', 'long_term']:
        print("range:", sp_range)

        results = sp.current_user_top_artists(time_range=sp_range, limit=50)

        for i, item in enumerate(results['items']):
            print(i, item['name'])
        print()

current_user_top_artist()