from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, SelectField
from wtforms.validators import DataRequired


class AppForm(FlaskForm):
    name = StringField("What's Your Name?", validators=[DataRequired()])
    submit = SubmitField("Submit")


class QuizForm(FlaskForm):
    mood_1 = SelectField('First Mood', choices=[("Happy", "Happy"), ("Sad", "Sad"), ("Irritable", "Irritable"), ("Loving", "Loving")], validators=[DataRequired()])
    submit = SubmitField("Submit")


class SecondChoice(FlaskForm):
    all_moods = {
        "Happy": ["Confident", "Inspired", "Joyful", "Pumped"],
        "Sad": ["Depressed", "Lonely", "Grief", "Heartbroken"],
        "Irritable": ["Frustrated", "Anxious", "Jealous", "Livid"],
        "Loving": ["Unrequited Love", "Playful", "Adoration", "Passionate"]
    }
    mood_2 = SelectField('First Mood', choices=[], validators=[DataRequired()])
    submit = SubmitField("Submit final mood")



    # mood_2 = SelectField('Second Mood', choices=[])
    # moods = {
    #     "H": ["Confident", "Inspired", "Joyful", "Pumped"],
    #     "S": ["Depressed", "Lonely", "Grief", "Heartbroken"],
    #     "I": ["Frustrated", "Anxious", "Jealous", "Livid"],
    #     "L": ["Unrequited Love", "Playful", "Adoration", "Passionate"]
    # }
    # all_moods = {
    #     "Happy": ["Confident", "Inspired", "Joyful", "Pumped"],
    #     "Sad": ["Depressed", "Lonely", "Grief", "Heartbroken"],
    #     "Irritable": ["Frustrated", "Anxious", "Jealous", "Livid"],
    #     "Loving": ["Unrequited Love", "Playful", "Adoration", "Passionate"]
    # }
