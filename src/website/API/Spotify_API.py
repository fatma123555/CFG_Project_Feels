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

""" 
    This is the class that is responsible for creating and sending requests to spotify using the spotipy library
"""
class SpotifyPlaylist():
    """
        The class constructor that will initialize all the key variables for the Spotify API class
    """
    def __init__(self):
        self.sp = spotipy.Spotify(client_credentials_manager=SpotifyClientCredentials(client_id, client_secret))
        self.playlists = None
        self.playlist_url = None
        self.playlist_id = None
        self.playlist_img = None
        self.playlist_name = None
        self.result = None

    """ 
        This function will get a random playlist returned back from spotify based on the mood provided as a search 
        parameter
        Returns:
            results dictionary
    """
    def send_request(self, mood):
        randomplaylist = random.randint(0, 1000)
        # send the request to spotify using spotipy
        results = self.sp.search(q=mood, limit=1, offset=randomplaylist, type="playlist", market=None)
        return results

    """ 
        This function will extract the results and find the playlists to save to that variable, and its name to be saved
        into the name variable list
    """
    def find_playlist(self, mood):
        # get the result of the request
        results = self.send_request(mood)
        # save the playlists to the playlists variable
        self.playlists = results['playlists']
        playlist_name = None
        for i, item in enumerate(self.playlists['items']):
            playlist_name = list((self.playlists['offset'] + i, item['name']))  # this returns the playlist names
        self.playlist_name = playlist_name

    """ 
        This function will extract the URL of the playlist into the playlist URL variable
    """
    def get_playlist_url(self):
        for i, item in enumerate(self.playlists['items']):
            playlist_url = list((self.playlists['offset'] + i, item['external_urls']))  # this returns the playlist url
            self.playlist_url = playlist_url

    """ 
        This function will extract the ID of the playlist into the playlist ID variable
    """
    def get_playlist_id(self):
        for i, item in enumerate(self.playlists['items']):
            playlist_id = list((self.playlists['offset'] + i, item['id'])) # this will return the ID
            self.playlist_id = playlist_id

    """ 
        This function will extract the IMG of the playlist into the playlist IMG variable
    """
    def get_playlist_image(self):
        for i, item in enumerate(self.playlists['items']):
            playlist_img = list((self.playlists['offset'] + i, item['images'])) # this will return the images
            self.playlist_img = playlist_img
    """ 
        This function will combine all the key extracted variables into a list containing the playlist name, the URL, 
        and the images
        Returns:
            a list, a list of key data regarding the playlist returned from the API call
    """
    def combining_all(self):
        combination = zip(self.playlist_name, self.playlist_url, self.playlist_img)
        playlist_name_url = list(combination)
        return playlist_name_url[1]
