try:
    from flask_wtf import FlaskForm
    from wtforms import StringField, SubmitField, SelectField, RadioField
    from wtforms.validators import DataRequired

    from src.website.database.data_manager import main_moods_tuples, all_moods
except Exception as e:
    print("Some modules are missing {}".format(e))

"""
    This class will create the first question form to be placed on the first page of the quiz
"""
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, SelectField, RadioField
from wtforms.validators import DataRequired

from src.website.database.data_manager import main_moods_tuples, all_moods

class QuizForm(FlaskForm):
    mood_1 = SelectField('How are you feeling?', choices=main_moods_tuples, validators=[DataRequired()])
    submit = SubmitField("Next")


"""
    This class will create the second question form to be placed on the second page of the quiz
"""


class SecondChoice(FlaskForm):
    all_moods = all_moods
    mood_2 = SelectField('Tell us how you really feel?', choices=[], validators=[DataRequired()])
    submit = SubmitField("Get my playlist!")


"""
    This class will create the rating form to be placed on the results page with the spotify embed playlist to its side
"""


class RatingForm(FlaskForm):
    radio = RadioField(u'How many stars? ',
                       choices=[('1', '⭐'), ('2', '⭐⭐'), ('3', '⭐⭐⭐'), ('4', '⭐⭐⭐⭐'), ('5', '⭐⭐⭐⭐⭐')],
                       validators=[DataRequired()])
    submit = SubmitField("Submit")
