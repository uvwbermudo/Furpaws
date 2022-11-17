from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, validators, SubmitField, SelectField
from wtforms.validators import Length, DataRequired, Email, EqualTo, Regexp


class LoginForm(FlaskForm):
    username = StringField(
        'User Name', 
        validators=[
            Length(min=10, max=50),
            DataRequired()
            ],
        )
    user_password = PasswordField(
        'Password', 
        validators=[
            DataRequired(message='Please enter a password')
            ],
        )

class RegisterForm(FlaskForm):
    email = StringField(
        'Email Address', 
        validators=[
            Length(min=10, max=50), 
            Email(message='Invalid Email'),
            DataRequired()
            ],
        )
    tag = StringField(
        'User Tag',
        validators=[
            Length(min=10, max=50),
            DataRequired()
        ]

        )
    password = PasswordField(
        'Password', 
        validators=[
            DataRequired(), 
            EqualTo('password2', message='Passwords must match')
            ]
        )
    password2 = PasswordField(
        'Confirm Password', 
        validators=[
            DataRequired(),
            EqualTo('password', message='Passwords must match')
            ]
        )
    account_type = SelectField('Account Type', choices = ['Pet Owner','Freelancer'])

    first_name = StringField(
        'First Name',
        validators=[
            Length(min=1, max=50), 
            DataRequired(message='First name is required'), 
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
            DataRequired(message='This field is required'), 
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
            DataRequired(message='This field is required'), 
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
            DataRequired(message='This field is required'), 
            Regexp(
                '\A\w+( \w+)*\Z', 
                message='Cannot submit, contains invalid characters',
                ),
            ],
        )
    country = StringField(
        'Country', 
        validators=[
            Length(min=1, max=12),
            DataRequired(message='This field is required'), 
            Regexp(
                '\A\w+( \w+)*\Z', 
                message='Cannot submit, contains invalid characters',
                ),
            ],
        )
    
