from flask_wtf import FlaskForm
from wtforms.validators import Length, DataRequired, Optional
from wtforms import TextAreaField, SubmitField

class AddFriend(FlaskForm):
    