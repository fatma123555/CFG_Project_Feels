try:
    # Spotify API
    import os
    from dotenv import load_dotenv

    # Credentials
    load_dotenv('.env')
    client_id = os.getenv('CLIENT_ID')
    client_secret = os.getenv('CLIENT_SECRET')


    import spotipy
    from spotipy.oauth2 import SpotifyClientCredentials
    import random
except Exception as e:
    print("Some modules are missing {}".format(e))

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

    def get_playlist_url(self):
        for i, item in enumerate(self.playlists['items']):
            playlist_url = list((self.playlists['offset'] + i, item['external_urls']))  # this returns the playlist url
            self.playlist_url = playlist_url

    def get_playlist_id(self):
        for i, item in enumerate(self.playlists['items']):
            playlist_id = list((self.playlists['offset'] + i, item['id']))
            self.playlist_id = playlist_id

    def get_playlist_image(self):
        # cover_img = self.sp.playlist_cover_image(self.playlist_id)
        for i, item in enumerate(self.playlists['items']):
            playlist_img = list((self.playlists['offset'] + i, item['images']))
            self.playlist_img = playlist_img

    def combining_all(self):
        combination = zip(self.playlist_name, self.playlist_url, self.playlist_img)
        playlist_name_url = list(combination)
        return playlist_name_url[1]

    def clear_search_query(self):
        pass

