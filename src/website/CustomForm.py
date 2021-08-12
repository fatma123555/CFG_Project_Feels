from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, SelectField, RadioField
from wtforms.validators import DataRequired

from src.website.database.data_manager import main_moods_tuples, all_moods

class AppForm(FlaskForm):
    name = StringField("What's Your Name?", validators=[DataRequired()])
    submit = SubmitField("Submit")


class QuizForm(FlaskForm):
    print(main_moods_tuples)
    mood_1 = SelectField('How are you feeling?', choices=main_moods_tuples, validators=[DataRequired()])
    submit = SubmitField("Next")


class SecondChoice(FlaskForm):
    all_moods = all_moods
    print(all_moods)
    mood_2 = SelectField('Tell us how you really feel?', choices=[], validators=[DataRequired()])
    submit = SubmitField("Get my playlist!")


class RatingForm(FlaskForm):
    radio = RadioField(u'How many stars? ', choices=[('1', '⭐'), ('2', '⭐⭐'), ('3', '⭐⭐⭐'), ('4', '⭐⭐⭐⭐'), ('5', '⭐⭐⭐⭐⭐')], validators=[DataRequired()])
    submit = SubmitField("Submit")
