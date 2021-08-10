from flask import Flask, render_template, flash, request, url_for, session
from werkzeug.utils import redirect

from src.website.CustomForm import AppForm, QuizForm, SecondChoice, RatingForm
from src.website.API.Spotify_API import SpotifyPlaylist

# Spotify API
import os
from dotenv import load_dotenv

# Credentials
load_dotenv('.env')
SECRET_KEY = os.getenv('SECRET_KEY')


def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = SECRET_KEY

    @app.route("/", methods=['GET', 'POST'])
    def home():
        name = None
        form = AppForm()
        # Validate the form submission
        if form.validate_on_submit():
            name = form.name.data
            form.name.data = ''
            flash("Form Submitted Successfully!")
        return render_template("index.html",
                               name=name,
                               form=form)

    @app.route("/quiz", methods=['GET', 'POST'])
    def quiz():
        form = QuizForm()
        answer = None
        if request.method == 'POST':
            answer = form.mood_1.data
            return redirect(url_for('quiz_second_question', mood=answer))
        return render_template("quiz.html", form=form, answer=answer)

    @app.route("/quiz/<mood>", methods=['GET', 'POST'])
    def quiz_second_question(mood):
        form = SecondChoice()
        form.mood_2.choices = form.all_moods[mood]
        if form.validate_on_submit():
            final_mood = form.mood_2.data
            playlist_finder = SpotifyPlaylist()
            playlist_finder.find_playlist(final_mood)
            playlist_finder.get_playlist_url()
            playlist_finder.get_playlist_image()
            response = playlist_finder.combining_all()
            playlist_code = response[1]['spotify'].split('/')[-1]
            playlist_data = {'URL': response[1]['spotify'],
                             'IMG-URL': response[2][0]['url'],
                             'CODE': playlist_code
                             }
            session['data'] = playlist_data
            return redirect(url_for('save_rating', final_mood=final_mood))
        return render_template("quiz_second_question.html", form=form, mood=mood)

    @app.route("/result/", methods=["GET", "POST"])
    def save_rating():
        # create rating form
        form = RatingForm()
        rating = None
        if form.validate_on_submit():
            rating = form.radio.data
            # # the user rating score
            # print(rating)
            # # the data that holds the URL for playlist, the IMG-URL and the playlist CODE
            # print(session['data'])
        return render_template("result.html", form=form, rating=rating, playlist_data=session['data'])

    @app.errorhandler(404)
    def page_not_found(e):
        return render_template("404.html"), 404

    return app
