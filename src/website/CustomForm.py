from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, SelectField, RadioField
from wtforms.validators import DataRequired


class AppForm(FlaskForm):
    name = StringField("What's Your Name?", validators=[DataRequired()])
    submit = SubmitField("Submit")


class QuizForm(FlaskForm):
    mood_1 = SelectField('How are you feeling?', choices=[("Happy", "Happy"), ("Sad", "Sad"), ("Irritable", "Irritable"), ("Loving", "Loving")], validators=[DataRequired()])
    submit = SubmitField("Next")


class SecondChoice(FlaskForm):
    all_moods = {
        "Happy": ["Confident", "Inspired", "Joyful", "Pumped"],
        "Sad": ["Depressed", "Lonely", "Grief", "Heartbroken"],
        "Irritable": ["Frustrated", "Anxious", "Jealous", "Livid"],
        "Loving": ["Unrequited Love", "Playful", "Adoration", "Passionate"]
    }
    mood_2 = SelectField('Tell us how you really feel?', choices=[], validators=[DataRequired()])
    submit = SubmitField("Get my playlist!")


class RatingForm(FlaskForm):
    radio = RadioField(u'How many stars? ', choices=[('1', '⭐'), ('2', '⭐⭐'), ('3', '⭐⭐⭐'), ('4', '⭐⭐⭐⭐'), ('5', '⭐⭐⭐⭐⭐')], validators=[DataRequired()])
    submit = SubmitField("Submit")
