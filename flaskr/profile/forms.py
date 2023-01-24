from flask_wtf import FlaskForm
from wtforms.validators import Length, DataRequired, Optional, Email, EqualTo, Regexp
from wtforms import TextAreaField, StringField, PasswordField, validators, SubmitField, SelectField
from wtforms.fields import FileField

class EditProfileForm(FlaskForm):
    email = StringField(
        'Email Address', 
        validators=[
            Length(min=10, max=50), 
            Email(message='Invalid Email')
            ],
        )
    tag = StringField(
        'User Tag',
        validators=[
            Length(min=5, max=30),
            Regexp(
                '\A[a-zA-Z0-9._-]+\Z', message="Only symbols: ' - _  . ' are allowed."
            )
        ]

        )
    
    old_pwd = PasswordField('Password', validators=[DataRequired(message='This field is required')])

    pwd = PasswordField(
        'Password', 
        validators=[
            EqualTo('pwd2', message='Passwords must match.')
            ]
        )
    pwd2 = PasswordField(
        'Confirm Password', 
        validators=[
            EqualTo('pwd', message='Passwords must match.')
            ]
        )
    first_name = StringField(
        'First Name',
        validators=[
            Length(min=1, max=50), 

            Regexp(
                '\A\w+( \w+)*\Z', 
                message='Cannot submit, contains invalid characters',
                ),
            ],
        )
    last_name = StringField(
        'Last Name', 
        validators=[
            Length(min=1, max=50),
            DataRequired(message='Last name is required'), 
            Regexp(
                '\A\w+( \w+)*\Z', 
                message='Cannot submit, contains invalid characters',
                ),
            ],
        )
    city = StringField(
        'City/Municipality', 
        validators=[
            Length(min=1, max=50),
            Regexp(
                '\A\w+( \w+)*\Z', 
                message='Cannot submit, contains invalid characters',
                ),
            ],
        )
    state = StringField(
        'State', 
        validators=[
            Length(min=1, max=50),
            Regexp(
                '\A\w+( \w+)*\Z', 
                message='Cannot submit, contains invalid characters',
                ),
            ],
        )
    zipcode = StringField(
        'Zip Code', 
        validators=[
            Length(min=1, max=12),
            Regexp(
                '\A\w+( \w+)*\Z', 
                message='Cannot submit, contains invalid characters',
                ),
            ],
        )
    country = StringField(
        'Country', 
        validators=[
            Regexp(
                '\A\w+( \w+)*\Z', 
                message='Cannot submit, contains invalid characters',
                ),
            ],
        )
    profile_pic = FileField()
