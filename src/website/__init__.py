from flask import Flask, render_template, request, url_for, session, abort
from werkzeug.utils import redirect
# import the key custom created form classes and the spotify API caller class
from src.website.CustomForm import QuizForm, SecondChoice, RatingForm
from src.website.API.Spotify_API import SpotifyPlaylist
# import the key methods for the data management within the app
from src.website import database
from src.website.database.feels_database import FeelsDatabase
# import the libraries to load the environment and its secrets
import os
from dotenv import load_dotenv

# load the environment secret variables
load_dotenv('.env')
SECRET_KEY = os.getenv('SECRET_KEY')

"""
    The main create_app method wrapper that will create the Flask app 
    Returns:
        app, the flask app
"""


def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = SECRET_KEY
    feels_database = FeelsDatabase()

    """"
        This method is responsible for returning the homepage 
        while also deleting any key data held within the session to 
        reset for the user to use our service
        Returns:
         index.html template
    """

    @app.route("/", methods=['GET', 'POST'])
    def home():
        # remove the data from the session if it is there
        try:
            session.pop('PATH', None)
            session.pop('SUB_MOOD', None)
            session.pop('code', None)
            session.pop('data', None)
            session.pop('my_var', None)
            session.pop('MAIN_MOOD', None)
        except Exception as e:
            print("Something is wrong with the session", e)
        return render_template("index.html")  # return the homepage

    """"
        This method is responsible for returning the first page of the  
        quiz and will collect the data from the form
        This specific method returns the first quiz question for the 
        recommendation system, so it sets the PATH to 'recommendation'
        Returns:
         quiz_second_question.html template if a POST method is called on submission of the form 
         or quiz.html to render the original first question page
    """

    @app.route("/quiz", methods=['GET', 'POST'])
    def quiz():
        # set the path to recommendation to know which route to load later on the flask app
        session['PATH'] = "recommendation"
        form = QuizForm()
        try:
            form.mood_1.choices = feels_database.get_main_moods()
        except Exception as e:
            print("Problem with setting the form choices {}".format(e))
        answer = None
        if request.method == 'POST':
            # get the answer, the main mood, from the form
            answer = form.mood_1.data
            session['MAIN_MOOD'] = answer
            return redirect(url_for('quiz_second_question',  # go to the second question
                                    mood=answer))
        return render_template("quiz.html",
                               form=form,
                               answer=answer)

    """"
        This method is responsible for returning the first page of the  
        quiz and will collect the data from the form
        This specific method returns the first quiz question for the 
        popular rated playlists, so it sets the PATH to 'popular'
        Returns:
            quiz_second_question.html template if a POST method is called on submission of the form 
            or quiz_popular.html to render the original first question page
    """

    @app.route("/quiz_popular", methods=['GET', 'POST'])
    def quiz_popular():
        # set the path to popular to know which route to load later on the flask app
        session['PATH'] = "popular"
        form = QuizForm()
        try:
            form.mood_1.choices = feels_database.get_main_moods()
        except Exception as e:
            print("Problem with setting the form choices {}".format(e))
        answer = None
        if request.method == 'POST':
            answer = form.mood_1.data  # get the answer to the first question, the main mood
            session['MAIN_MOOD'] = answer
            return redirect(url_for('quiz_second_question',  # load the second question page
                                    mood=answer))
        return render_template("quiz_popular.html",
                               form=form,
                               answer=answer,
                               path=session['PATH'])

    """"
        This method is responsible for returning the second page of the  
        quiz and will collect the data from the form
        This specific method returns the second quiz question and saves the answers to the session
        Returns:
            save_rating is called if the route takes is the 'recommendation' path
            or popular_playlists is called if the path is 'popular'
            or mainly will return the quiz_second_question.html page with the form loaded on it
    """

    @app.route("/quiz/<mood>", methods=['GET', 'POST'])
    def quiz_second_question(mood):
        form = SecondChoice()
        try:
            form.mood_2.choices = form.all_moods[mood]
        except Exception as e:
            print("Problem with setting the second question form choices {}".format(e))
        if form.validate_on_submit():
            final_mood = form.mood_2.data  # get the answer to the sub mood chosen
            packager = PlaylistDataPackager()  # initialise the playlist data packager
            response = packager.get_playlist_response(final_mood)
            # if something went wrong with the request, then redirect to the 404 page
            if response is None:
                abort(404, description="Resource not found")
            playlist_data = packager.get_playlist_data(response)  # a dictionary of data is returned
            session['data'] = playlist_data
            session['SUB_MOOD'] = final_mood
            # the playlist is added to the database for usage and reference later
            feels_database.add_playlist(playlist_data['NAME'], playlist_data['URL'], session['MAIN_MOOD'], session['SUB_MOOD'])
            if session['PATH'] == 'recommendation':
                # if the path was recommendation, then a random playlist is shown on the screen for the user to rate
                return redirect(url_for('save_rating',
                                        final_mood=final_mood))
            else:
                # else if popular was chosen, then the top 3 rated saved playlists will be shown instead if they exists
                # else an post is put on the screen saying otherwise and the use is redirected back to the homepage
                # through a button on the screen
                return redirect(url_for('popular_playlists',
                                        final_mood=final_mood))
        return render_template("quiz_second_question.html",  # load the second question and its form to the page
                               form=form,
                               mood=mood)

    """"
        This method is responsible for returning the results page with a spotify playlist from the request made 
        as well as a rating form to rate the playlist on the screen, with options to go back home
        The score is updated when the user submits the rating using the form on the page which is saved to the database
        Returns:
            result.html template page
    """

    @app.route("/result/", methods=["GET", "POST"])
    def save_rating():
        # create rating form
        form = RatingForm()
        rating = None
        playlist_data = session['data']
        final_mood = session['SUB_MOOD']
        if form.validate_on_submit():
            rating = form.radio.data # get the voted rating score
            # update the score of that playlist in the database, else add it to the database with it score
            feels_database.update_score(playlist_data['NAME'], playlist_data['URL'], rating)
        return render_template("result.html",  # return the result page with the rating form
                               form=form,
                               rating=rating,
                               playlist_data=playlist_data,
                               final_mood=final_mood)

    """"
        This method is responsible for returning the top three rated playlists based on a specific mood on the page,
        however if the database does not find at least 3 top rated playlists, then it redirects the user to an error 
        page showing that there were no results with an option to go home
        Returns:
            popular_playlists.html template page, but will show no_playlists_found.html page if not enough playlists 
            were rated for that specific mood
    """

    @app.route("/popular_playlists", methods=["GET", "POST"])
    def popular_playlists():
        """
        this function will be used to call and calculate the popular playlists from the database.
        and output the result to the screen on the highly rated page
        """
        # get the top rated playlists based on the sub_mood, will be empty if there aren't any saved, or
        # if there aren't enough saved playlists to make up a top 3
        top_scores_dict = feels_database.get_top_scores_dict(session['SUB_MOOD'])
        if len(top_scores_dict) == 0:  # if its an empty dict, then tell the user that no playlists were found
            return render_template("no_playlists_found.html")
        return render_template("popular_playlists.html",  # return the popular playlists top 3 in a list
                               top_scores_dict=top_scores_dict,
                               final_mood=session['SUB_MOOD'],
                               path=session['PATH'])

    """"
        This method is responsible for returning the page with the playlist that the user clicked on from the previous 
        page which is the list of popular playlists based on the mood chosen from the quiz
        This page is only rendered if there are 3 top rated playlists stored in the database based on the mood chosen
        Returns:
            popular_result.html template page
    """

    @app.route("/popular_playlist_result/<num>", methods=["GET", "POST"])
    def popular_playlist_result(num):
        final_mood = session['SUB_MOOD']
        # get the top 3 scoring playlists
        top_scores_dict = feels_database.get_top_scores_dict(session['SUB_MOOD'])
        return render_template("popular_result.html",  # showcase the clicked playlist on screen
                               top_three=top_scores_dict,
                               num=int(num),
                               final_mood=final_mood)

    """ 
    This method was created to handle the error pages that could occur in terms of a 404 error page.
    Returns:
        404.html
    """

    @app.errorhandler(404)
    def page_not_found(e):
        return render_template("404.html"), 404  # show a custom 404 error page

    return app


""" 
    This class is responsible for creating a playlist data packager that will extract the returned response dictionary 
    into a dictionary that contains the necessary data to be used in the Flask app, the URL, IMG-URL, CODE (for the 
    embed on the results page), the NAME of the playlist

"""


class PlaylistDataPackager():
    """
        This method is responsible for creating and getting an API response by using the SpotifyPlaylist python module.
        Returns:
            a response dictionary
    """

    def get_playlist_response(self, final_mood):
        try:
            # create the object to handle the request
            playlist_finder = SpotifyPlaylist()
            # send the request to the Spotify
            playlist_finder.find_playlist(final_mood)
            playlist_finder.get_playlist_url()
            playlist_finder.get_playlist_image()
            # use the combine all method to combine the data received from the request into a dictionary
            response = playlist_finder.combining_all()
            return response
        except Exception as e:
            print("Problem with sending a spotify API request {}".format(e))

    """ 
        This method is responsible for extracting the key information from the response dictionary into usable 
        data for the Flask app 
        Returns:
            playlist_data, a dictionary of data
    """

    def get_playlist_data(self, response):
        # extract the data from the response into data to be used within the flask app and embeds in the templates
        playlist_data = {'URL': response[1]['spotify'],
                         'IMG-URL': response[2][0]['url'],
                         'CODE': response[1]['spotify'].split('/')[-1],
                         'NAME': response[0]
                         }
        return playlist_data
