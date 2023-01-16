from flask_wtf import FlaskForm
from wtforms.validators import Length, DataRequired, Optional
from wtforms import TextAreaField, SubmitField
from wtforms.fields import FileField


class AddPostForm(FlaskForm):
    post_description = TextAreaField('Enter description: ', validators=[
                                     Length(max=150), Optional()])
    add_photos = FileField("Add Photos")
    add_videos = FileField("Add Videos")
    add_post_button = SubmitField("Add Post")



class EditPostForm(FlaskForm):
    post_description = TextAreaField(validators=[
        Length(max=150), Optional()])
    add_photos = FileField("Add Photos")
    add_videos = FileField("Add Videos")
    edit_post_button = SubmitField("Save changes")


class EditCommentForm(FlaskForm):
    edit_comment_textbox = TextAreaField(validators=[
        Length(max=150), Optional()])
    edit_comment_button = SubmitField("Edit Comment")
