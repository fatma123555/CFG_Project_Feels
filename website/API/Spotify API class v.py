# Spotify API
import spotipy
import sys
from spotipy.oauth2 import SpotifyClientCredentials
from spotifysecret import *
import random


class SpotifyPlaylist():
    def __init__(self):
        pass

    def find_playlist(self, mood):
        randomplaylist = random.randint(0, 1000)
        sp = spotipy.Spotify(client_credentials_manager=SpotifyClientCredentials(client_id, client_secret))
        self.sp = sp
        results = self.sp.search(q=mood, limit=1, offset=randomplaylist, type="playlist", market=None)
        self.playlists = results['playlists']
        for i, item in enumerate(self.playlists['items']):
            playlist_name = list((self.playlists['offset'] + i, item['name']))  # this returns the playlist names
        self.playlist_name = playlist_name
        # print(self.playlist_name)

    def get_playlist_url(self):
        for i, item in enumerate(self.playlists['items']):
            playlist_url = list((self.playlists['offset'] + i, item['external_urls']))  # this returns the playlist url
            self.playlist_url = playlist_url
            # print(self.playlist_url)

    def get_playlist_id(self):
        for i, item in enumerate(self.playlists['items']):
            playlist_id = list((self.playlists['offset'] + i, item['id']))
            self.playlist_id = playlist_id

    def get_playlist_image(self):
        # cover_img = self.sp.playlist_cover_image(self.playlist_id)
        for i, item in enumerate(self.playlists['items']):
            playlist_img = list((self.playlists['offset'] + i, item['images']))
            self.playlist_img = playlist_img
            # print(self.playlist_img)

    def combining_all(self):
        combination = zip(self.playlist_name, self.playlist_url, self.playlist_img)
        playlist_name_url = list(combination)
        print(playlist_name_url[1])

    def clear_search_query(self):
        pass


finding_spotify_playlist1 = SpotifyPlaylist()
finding_spotify_playlist1.find_playlist('happy')
finding_spotify_playlist1.get_playlist_url()
finding_spotify_playlist1.get_playlist_image()
finding_spotify_playlist1.combining_all()