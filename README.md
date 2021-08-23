
# CFG Capstone Project: Feels
Capstone project created with a team of 5 other CodeFirst Girls Nanodegree students that is an accumulation of all the skills gained from the program to contribute to the final grade of the Nanodegree and display the coding epxerience gained and learned.


# Feels
*Get in your feels*

Feels is an application that allows you to explore your current mood with a playlist selected for you at random, using a mood quiz. 

**Installing / Getting started:** <br />
A quick introduction of the minimal setup you need to get Feels up & running.

pip3 install flask <br />
pip3 install Flask_WTF <br />
pip3 install spotipy  <br />
pip3 install Python-dotenv <br />
pip3 install pandas <br />
pip3 install os_sys <br />
pip3 install WTForms <br />
pip3 install Werkzeug <br />
pip3 install pathlib <br />
pip3 install unittest2 <br />


**Initial Configuration:**  <br />
For conifgurationg purposes a separate .env file will need to be created that will need to hold secret keys. <br />
CLIENT_ID = "**********" <br />
CLIENT_SECRET = "*************" <br />
SECRET_KEY = "*************"

**User Tutorial:** <br />
![user_tutorial_gif](https://github.com/fatma123555/CFG_Project_Feels/blob/c1f3e8109bb0586d76ebe4868210dd8cc52fb290/playlist_quiz_recommendation.gif)

Click the links to view videos of how to use the app!

[Getting a recommended playlist](https://youtu.be/BUZbUu5Q60E)

[Find User Rated Popular Playlists](https://youtu.be/zxvp_0TLrH0)

[Future Login Feature](https://youtu.be/zxvp_0TLrH0)

**Deploying / Publishing:** <br />
For future development of this project, it would be ideal to be able to publish the project onto Heroku

**Features:**  <br />
The main features of this project is being given a randomly selected playlist based off the results of the quiz, using the spotipy api. <br />
You can also set a rating on the randomly selected playlist which will then be stored in the database.<br />
These ratings can be used to pull the most popular playlists within the selected moods. <br />
future work feature: admin section for updating and adding moods to app<br />


**Contributing:** <br />
If you'd like to contribute, please fork the repository and use a feature branch. Pull requests are warmly welcome.
