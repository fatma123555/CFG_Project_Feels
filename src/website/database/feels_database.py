try:
    # Read entire moods file
    import pandas as pd
    from pathlib import Path

    data_folder = Path("./website/database/")
    moods_path = data_folder / "moods.csv"
except Exception as e:
    print("Some modules are missing {}".format(e))
# print(moods_path)
# file = pd.read_csv(moods_path)

# # Read only playlist name and score
# # import pandas as pd
# file = pd.read_csv('playlist_score.csv', skipinitialspace=True, usecols=['PLAYLIST NAME', 'SCORE'])
# print(file)

# def read_csv(path):
#     pd_read =

# Read both playlist mood and score (JOIN function)
# import pandas as pd
# pmood = pd.read_csv('playlist_mood.csv')
# pscore = pd.read_csv('playlist_score.csv')
# output1 = pd.merge(pmood, pscore,
#                    on=['playlist_name','URL'],
#                    how='inner')
# print(output1)
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

# print(get_main_moods())

""" 
method that will get and return the values in a specific column and return it as a list
"""
def get_sub_moods(main_mood):
    with open(moods_path, 'r') as f:
        pd_reader = pd.read_csv(f)
    results = [x for x in pd_reader[main_mood].values if str(x) != 'nan']
    return results

# print(get_sub_moods("happy"))
# print(file)
# add_new_mood("Angry", ["livid", "furious", "resentful"])
# print("*" * 30)
# print("*" * 30)
# file = pd.read_csv(moods_path)
# print(file)
# print("*" * 30)
# print("*" * 30)
# print("get main moods:", get_main_moods())
# print("Get the sub mood for Angry:",get_sub_moods("Angry"))

# # function to add new descriptive words to existing main moods
# def add_mood(happy, sad, irritable, loving):
#     from csv import writer
#     List=[happy, sad, irritable, loving]
#     with open(moods_path, 'a') as f_object:
#         writer_object = writer(f_object)
#         writer_object.writerow(List)
#         f_object.close()

# add_mood('ecstatic', 'miserable', 'terrible', 'sweet')

data_folder = Path("./website/database/")
playlist_score_path = data_folder / "playlist_score.csv"
data_folder = Path("./website/database/")
playlist_mood_path = data_folder / "playlist_mood.csv"
# print(playlist_mood_path)

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


#add_playlist('nameA', 'URLA', 'loving', 'heartbroken')

# print(playlist_score_path)

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


# # Return all playlists based on a specific sub-mood
# def all_by_mood(mood):
#     import pandas as pd
#     file=pd.read_csv(r"playlist_mood.csv")
#     file_mood = file[file['sub_mood'] == mood]
#     print(file_mood)

# all_by_mood('depressed')

#Return top 3 highest scoring playlist (any mood)
def top_scores():
    import pandas as pd
    pmood = pd.read_csv(playlist_mood_path)
    pscore = pd.read_csv(playlist_score_path)
    output1 = pd.merge(pmood, pscore,
                       on=['playlist_name','URL'],
                       how='inner')
    output1.sort_values(["score"],
                        axis=0,
                        ascending=[False],
                        inplace=True)
    top_three = output1[:3]
    indexes = top_three.index.values.tolist()
    return indexes, top_three


def get_top_scores_dict():
    indexes, top_three = top_scores()
    first = top_three.loc[int(indexes[0])]
    second = top_three.loc[int(indexes[1])]
    third = top_three.loc[int(indexes[2])]
    # saves the playlists in order with details: [playlist_name, URL, main_mood, sub_mood, score] in a list
    scores_dict = {
        1: [first['playlist_name'], first['URL'], first['main_mood'], first['sub_mood'], first['score']],
        2: [second['playlist_name'], second['URL'], second['main_mood'], second['sub_mood'], second['score']],
        3: [third['playlist_name'], third['URL'], third['main_mood'], third['sub_mood'], third['score']]
    }

    print("FIRST:\n", scores_dict[1])
    print("SECOND:\n", scores_dict[2])
    print("THIRD:\n", scores_dict[3])

    return scores_dict

print("TOP_SCORES\n", get_top_scores_dict())



# # Return top 3 playlists by score based on mood
# def top_by_mood(mood):
#     import pandas as pd
#     pmood = pd.read_csv('playlist_mood.csv')
#     pscore = pd.read_csv('playlist_score.csv')
#     data = pd.merge(pmood, pscore,
#                     on=['playlist_name','URL'],
#                     how='inner')
#     data.sort_values("main_mood", inplace = True)
#     filter1 = data["main_mood"]==mood
#     data.where(filter1, inplace = True)
#     data.sort_values(["score"],
#                     axis=0,
#                     ascending=[False],
#                     inplace=True)
#     data = data.dropna()
#     print(data[:3])

# top_by_mood('happy')


# # Function to add new main emotion


