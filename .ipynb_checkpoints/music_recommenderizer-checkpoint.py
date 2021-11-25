import pandas as pd
from random import randint
import pickle
from sklearn.cluster import KMeans
from sklearn import cluster
from sklearn.preprocessing import StandardScaler
import numpy as np
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials


class Error(Exception):
    """Base class for other exceptions"""
    pass

class SongEmpty(Error):
    """Raised when the input value is empty"""
    pass

class ArtistEmpty(Error):
    """Raised when the input value is empty"""
    pass

def user_pick_song():
    while True:
        try: 
            song = str(input("Enter a song you like: "))
            if song == '':
                raise SongEmpty
            break
        except SongEmpty:
            print("no song entered, please enter a song")
    return song

def use_pick_artist():
    while True:
        try: 
            artist = str(input("Enter the artist: "))
            if artist == '':
                raise ArtistEmpty
            break
        except ArtistEmpty:
            print("You didn't enter an artist")
    return artist

def is_song_artist_hot(song, artist):
    for i in range(len(top100)):
        if (artist == top100['artist'][i].lower()) & (song == top100['song_title'][i].lower()):
            return True
    return False

def select_hot_song(song, artist):
    r_song = top100['song_title'][randint(0,len(top100))].lower()
    r_artist = top100['artist'][randint(0,len(top100))].lower()
    while r_song == song:
        r_song = top100['song_title'][randint(0,len(top100))].lower()
        r_artist = top100['artist'][randint(0,len(top100))].lower()
    return r_song, r_artist

def get_name_artist_meta_from_item(item,playlist_name,playlist_id):
    tracks_meta = {}
    tracks_meta['playlist_name'] = playlist_name
    tracks_meta['playlist_id'] = playlist_id
    tracks_meta['song_title'] = item["name"]
    tracks_meta['artist'] = item["artists"][0]["name"]
    tracks_meta = tracks_meta | sp.audio_features(item["uri"])[0]
    return tracks_meta



# load all the things
top100 = pd.read_csv('top_100.csv')
spotify_music_tracks_with_cluster = pd.read_csv('tracks_clustered.csv')
my_scaler = pickle.load(open('my_scaler.p','rb'))
my_model = pickle.load(open('my_model.p','rb'))

# SpotifyClientCredentials has no arguments as SPOTIPY_CLIENT_ID and SPOTIPY_CLIENT_SECRET are set in environment variables
sp = spotipy.Spotify(client_credentials_manager=SpotifyClientCredentials())


# checks if song is in Billboard 100 or not
user_song = user_pick_song()
user_artist = use_pick_artist()
user_is_hot = is_song_artist_hot(user_song,user_artist)
if user_is_hot:
    r_song, r_artist = select_hot_song(user_song, user_artist)
    display(f"Amazing AI recommends song from Billboard Top 100: {r_song.title()} by {r_artist.title()}")
else:
    print("We didn't find your song in Billboard Top 100, perhaps you would like to listen to...")

    results = sp.search(q=user_song + ' ' + user_artist, type="track", market="US", limit=1)
    user_song_meta = get_name_artist_meta_from_item(results["tracks"]["items"][0], "User Search", 99)
    #user_song_meta = pd.DataFrame(user_song_meta)
    user_song_meta
    x = []
    x.append(user_song_meta)
    user_song_meta = pd.DataFrame(x)
    user_song_meta_num = user_song_meta.select_dtypes(np.number)
    user_song_meta_num = user_song_meta_num.drop(["playlist_id"],axis=1)
    user_song_meta_num = my_scaler.transform(user_song_meta_num)
    track_from_same_cluster = spotify_music_tracks_with_cluster[spotify_music_tracks_with_cluster['cluster_assigned']==my_model.predict(user_song_meta_num)[0]].sample(1)
    # while song same, select new song
    #     track_from_same_cluster = spotify_music_tracks_with_cluster[spotify_music_tracks_with_cluster['cluster_assigned']==my_model.predict(user_song_meta_num)[0]].sample(1)
    
    print("track_from_same_cluster[['song_title']].iloc[0,0] + " by " + track_from_same_cluster[['artist']].iloc[0,0])