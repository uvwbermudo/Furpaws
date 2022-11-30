from flask_wtf import FlaskForm
from wtforms.validators import Length, DataRequired
from wtforms import TextAreaField, SubmitField
from wtforms.fields import FileField


class AddPostForm(FlaskForm):
    post_description = TextAreaField('Enter description: ', validators=[
                                     Length(max=150), DataRequired()])
    add_photos = FileField("Add Photos")
    add_videos = FileField("Add Videos")
    add_post_button = SubmitField("Add Post")
    edit_post_button = SubmitField("Save changes")
