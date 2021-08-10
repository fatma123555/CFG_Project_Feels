from flask import Flask, render_template, flash, request, url_for
from werkzeug.utils import redirect

from src.website.CustomForm import AppForm, QuizForm, SecondChoice

def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = 'This is my test secret key'

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
            return render_template("result.html", final_mood=final_mood)
        return render_template("quiz_second_question.html", form=form, mood=mood)

    @app.errorhandler(404)
    def page_not_found(e):
        return render_template("404.html"), 404

    return app
