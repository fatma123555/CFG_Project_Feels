try:
    # Read entire moods file
    import pandas as pd
    from pathlib import Path

    data_folder = Path("./website/database/")
    moods_path = data_folder / "moods.csv"
    playlist_score_path = data_folder / "playlist_score.csv"
    playlist_mood_path = data_folder / "playlist_mood.csv"
except Exception as e:
    print("Some modules are missing {}".format(e))
import pandas as pd
from pathlib import Path

data_folder = Path("./website/database/")
moods_path = data_folder / "moods.csv"
playlist_score_path = data_folder / "playlist_score.csv"
playlist_mood_path = data_folder / "playlist_mood.csv"
"""
    This class will create the main database component and will mock the queries that would have been sent to a database
    It is responsible for retrieving the data, for storing the data, and for updating the scores 
"""


class FeelsDatabase():
    """
        The init file will initialise the paths necessary for functions of this class
    """

    def __init__(self):
        self.data_folder = Path("./website/database/")
        self.moods_path = self.data_folder / "moods.csv"
        self.playlist_score_path = self.data_folder / "playlist_score.csv"
        self.playlist_mood_path = self.data_folder / "playlist_mood.csv"

    """ 
        method that will add a new mood as a header and fill the values of that 
        column with a list of sub_moods, if it isn't long enough, then the values
        will be NaN values
    """

    def add_new_mood(self, main_mood, sub_moods):
        df = pd.read_csv(self.moods_path)
        df[main_mood] = pd.Series(sub_moods)
        df.to_csv(moods_path, index=False)

    """ 
        method that will get and return the headers and return it as a list
        Returns:
            a list, list of the main moods currently stored in the 'database'
    """

    def get_main_moods(self):
        with open(self.moods_path, 'r') as f:
            pd_reader = pd.read_csv(f)
            # make sure to convert it to a list before returning to have a list of main moods
            return list(pd_reader.head())

    """ 
        method that will get and return the values in a specific column and return it as a list
        Returns:
           a list, a list of all the sub-moods of a specific mood from the 'database' 
    """

    def get_sub_moods(self, main_mood):
        with open(self.moods_path, 'r') as f:
            pd_reader = pd.read_csv(f)
        # filter out the NaN values in the table
        results = [x for x in pd_reader[main_mood].values if str(x) != 'nan']
        return results

    """ 
        This function will add new playlist not already in the CSV file to save the playlist and its moods
    """

    def add_playlist(self, name, URL, main_mood, sub_mood):
        df = pd.read_csv(self.playlist_mood_path)
        # if the playlist is not already in the table
        if URL not in [str(url) for url in df.URL]:
            new_row = {"playlist_name": name,
                       "URL": URL,
                       "main_mood": main_mood,
                       "sub_mood": sub_mood}
            # we add it to the table that holds all the playlists and their moods
            df = df.append(new_row, ignore_index=True)
        df.to_csv(self.playlist_mood_path, index=False)

    """
        This function will update the score if the playlist exists in the table, else it will add a new entry to the  
        table with its score
    """

    def update_score(self, name, URL, new_score):
        df = pd.read_csv(self.playlist_score_path)
        if URL in [str(url) for url in df.URL]:
            # update the score if playlist is in the table
            df.loc[df["URL"] == URL, "score"] += new_score
        else:
            # else add the playlist entry to the table with its associated score
            new_row = {"playlist_name": name,
                       "URL": URL,
                       "score": new_score}
            df = df.append(new_row, ignore_index=True)
        df.to_csv(self.playlist_score_path, index=False)

    """
        This function will find the top scoring stored playlists in the 'database' by merging the two tables playlist_mood 
        and playlist_score, filtered on the specific mood we are looking for
    """

    def top_scores(self, sub_mood):
        import pandas as pd
        pmood = pd.read_csv(self.playlist_mood_path)
        pscore = pd.read_csv(self.playlist_score_path)
        # mocking the SQL JOIN query in joining the two tables needed, playlist mood and the playlist score table
        output1 = pd.merge(pmood, pscore,
                           on=['playlist_name', 'URL'],
                           how='inner')
        # create a variable to use as a filter
        is_sub_mood = output1['sub_mood'] == sub_mood
        # filter the rows by the sub_mood we are looking for only
        output1 = output1[is_sub_mood]
        # sort the rows by highest scoring to lowest
        output1.sort_values(["score"],
                            axis=0,
                            ascending=[False],
                            inplace=True)
        # save the top 3 scoring rows
        top_three = output1[:3]
        # save the indexes of these rows in order to call and refer to them in the Flask app and jinja HTML template
        indexes = top_three.index.values.tolist()
        return indexes, top_three

    """
        This function will return a dictionary with the top three scoring playlists based on the mood from the top_scores 
        function, but will return an empty dictionary if there aren't 3 scoring playlists. This method will format the 
        data specifically to be used in the Flask app and the jinja templates to be embedded on screen
        Returns:
            a dictionary, either empty or filled with the top three playlists
    """

    def get_top_scores_dict(self, sub_mood):
        # get the indexes and the top 3 playlists by the sub mood as a dataframe
        indexes, top_three = self.top_scores(sub_mood)
        # reject any dataframe less than 3, as we need the top 3 rated playlists, return an empty dict otherwise
        if len(top_three) < 3:
            empty_dict = dict()
            return empty_dict
        # set the first, second and third rows to variables using the indexes
        first = top_three.loc[int(indexes[0])]
        second = top_three.loc[int(indexes[1])]
        third = top_three.loc[int(indexes[2])]
        # saves the playlists in order with details: [playlist_name, URL, main_mood, sub_mood, score] in a list
        scores_dict = {
            1: [first['playlist_name'], first['URL'], first['main_mood'], first['sub_mood'], first['score']],
            2: [second['playlist_name'], second['URL'], second['main_mood'], second['sub_mood'], second['score']],
            3: [third['playlist_name'], third['URL'], third['main_mood'], third['sub_mood'], third['score']]
        }

        return scores_dict
