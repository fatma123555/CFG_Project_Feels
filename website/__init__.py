from flask import Flask, render_template, flash
from website.CustomForm import AppForm


def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = 'This is my test secret key'

    @app.route("/", methods=['GET', 'POST'])
    def home():
        name = None
        form = AppForm()
        # Validate the form submision
        if form.validate_on_submit():
            name = form.name.data
            form.name.data = ''
            flash("Form Submitted Successfully!")
        return render_template("index.html",
                               name=name,
                               form=form)

    @app.route("/quiz", methods=['GET', 'POST'])
    def quiz():
        return render_template("quiz.html")

    @app.errorhandler(404)
    def page_not_found(e):
        return render_template("404.html"), 404

    return app
