import spotipy
from spotipy import SpotifyOAuth
#import credentials

#run the blow commands in your terminal before running this code
'''
export SPOTIPY_CLIENT_ID='your-spotify-client-id'
export SPOTIPY_CLIENT_SECRET='your-spotify-client-secret'
export SPOTIPY_REDIRECT_URI='your-app-redirect-url'
'''

scope = "user-modify-playback-state, user-read-currently-playing"
def pause_play():
    #determine if a song is currenly playing, and if so pause or play accordingly
    sp = spotipy.Spotify(auth_manager=SpotifyOAuth(scope=scope))
    song_info = sp.currently_playing()
    is_playing = song_info.get('is_playing')

    if is_playing:
        sp.pause_playback()
        return 1
    else:
        sp.start_playback()
        return 0




