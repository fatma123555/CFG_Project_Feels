# # Read entire moods file
# import pandas as pd
# file = pd.read_csv('moods.csv')
# print(file)

# # Read only playlist name and score
# import pandas as pd
# file = pd.read_csv('playlist_score.csv', skipinitialspace=True, usecols=['PLAYLIST NAME', 'SCORE'])
# print(file)

# # Read both playlist mood and score (JOIN function)
# import pandas as pd
# pmood = pd.read_csv('playlist_mood.csv')
# pscore = pd.read_csv('playlist_score.csv')
# output1 = pd.merge(pmood, pscore, 
#                    on=['playlist_name','URL'], 
#                    how='inner')
# print(output1)



# # function to add new descriptive words to existing main moods
# def add_mood(happy, sad, irritable, loving):
#     from csv import writer
#     List=[happy, sad, irritable, loving]
#     with open('moods.csv', 'a') as f_object:
#         writer_object = writer(f_object)
#         writer_object.writerow(List)
#         f_object.close()

# add_mood('ecstatic', 'miserable', 'terrible', 'sweet')


# # function to add new playlist not already in the CSV file
# def add_playlist(name, URL, main_mood, sub_mood):
#     from csv import writer
#     List=[name,URL,main_mood,sub_mood]
#     with open('playlist_mood.csv', 'a') as f_object:
#         writer_object = writer(f_object)
#         writer_object.writerow(List)
#         f_object.close()

# add_playlist('nameA', 'URLA', 'loving', 'heartbroken')


# function to update the score - adds new score to existing score
def update_score(URL, new_score):
    import pandas as pd
    df = pd.read_csv("playlist_score.csv")
    #df.set_value(1, "Score", 30)
    df.loc[df["URL"]==URL, "score"] += new_score
    df.to_csv("playlist_score.csv", index=False)

update_score('URLA', 4)
import pandas as pd
file = pd.read_csv('playlist_score.csv')
print(file)

# # Return all playlists based on a specific sub-mood
# def all_by_mood(mood):
#     import pandas as pd
#     file=pd.read_csv(r"playlist_mood.csv")
#     file_mood = file[file['sub_mood'] == mood]
#     print(file_mood)

# all_by_mood('depressed')


# #Return top 3 highest scoring playlist (any mood)
# def top_scores():
#     import pandas as pd
#     pmood = pd.read_csv('playlist_mood.csv')
#     pscore = pd.read_csv('playlist_score.csv')
#     output1 = pd.merge(pmood, pscore, 
#                     on=['playlist_name','URL'], 
#                     how='inner')
#     output1.sort_values(["score"], 
#                         axis=0,
#                         ascending=[False], 
#                         inplace=True)
#     print(output1[:3])
# top_scores()



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



