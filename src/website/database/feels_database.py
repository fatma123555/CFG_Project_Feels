try:
    # Read entire moods file
    import pandas as pd
    from pathlib import Path

    data_folder = Path("./website/database/")
    moods_path = data_folder / "moods.csv"
except Exception as e:
    print("Some modules are missing {}".format(e))

""" 
    method that will add a new mood as a header and fill the values of that 
    column with a list of sub_moods, if it isn't long enough, then the values
    will be NaN values
"""
def add_new_mood(main_mood, sub_moods):
    df = pd.read_csv(moods_path)
    df[main_mood] = pd.Series(sub_moods)
    df.to_csv(moods_path, index=False)

""" 
    method that will get and return the headers and return it as a list
"""
def get_main_moods():
    with open(moods_path, 'r') as f:
        pd_reader = pd.read_csv(f)
        return list(pd_reader.head())


""" 
    method that will get and return the values in a specific column and return it as a list
"""
def get_sub_moods(main_mood):
    with open(moods_path, 'r') as f:
        pd_reader = pd.read_csv(f)
    results = [x for x in pd_reader[main_mood].values if str(x) != 'nan']
    return results

data_folder = Path("./website/database/")
playlist_score_path = data_folder / "playlist_score.csv"
data_folder = Path("./website/database/")
playlist_mood_path = data_folder / "playlist_mood.csv"

# function to add new playlist not already in the CSV file to save the playlist and its moods
def add_playlist(name, URL, main_mood, sub_mood):
    df = pd.read_csv(playlist_mood_path)
    if URL not in [str(URL) for URL in df.URL]:
        new_row = {"playlist_name": name,
                   "URL": URL,
                   "main_mood": main_mood,
                   "sub_mood": sub_mood}
        df = df.append(new_row, ignore_index=True)
    df.to_csv(playlist_mood_path, index=False)

# function to update the score - adds new score to existing score
def update_score(name, URL, new_score):
    import pandas as pd
    df = pd.read_csv(playlist_score_path)
    if URL in [str(URL) for URL in df.URL]:
        # df.set_value(1, "Score", 30)
        df.loc[df["URL"] == URL, "score"] += new_score
    else:
        new_row = {"playlist_name": name,
                   "URL": URL,
                   "score": new_score}
        df = df.append(new_row, ignore_index=True)
    df.to_csv(playlist_score_path, index=False)

#Return top 3 highest scoring playlist (any mood)
def top_scores(sub_mood):
    import pandas as pd
    pmood = pd.read_csv(playlist_mood_path)
    pscore = pd.read_csv(playlist_score_path)
    output1 = pd.merge(pmood, pscore,
                       on=['playlist_name','URL'],
                       how='inner')
    is_sub_mood = output1['sub_mood'] == sub_mood
    output1 = output1[is_sub_mood]
    output1.sort_values(["score"],
                        axis=0,
                        ascending=[False],
                        inplace=True)
    top_three = output1[:3]
    indexes = top_three.index.values.tolist()
    return indexes, top_three


def get_top_scores_dict(sub_mood):
    indexes, top_three = top_scores(sub_mood)
    if len(top_three) < 3:
        empty_dict = dict()
        return empty_dict
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



