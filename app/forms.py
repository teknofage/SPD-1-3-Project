from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField, TextAreaField, SelectField
from wtforms.validators import ValidationError, DataRequired, Email, EqualTo, Length
from app.models import User


class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember_me = BooleanField('Remember Me')
    submit = SubmitField('Sign In')


class RegistrationForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    password2 = PasswordField(
        'Repeat Password', validators=[DataRequired(), EqualTo('password')])
    group = SelectField("Choose your Company: ", choices=[('blue', 'Blue Squares'),
                                                          ('red', 'Red Dragons'),
                                                          ('green', 'Green Scales'),
                                                          ('purple', 'Purple Royals')], default='blue')
    submit = SubmitField('Register')

    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        if user is not None:
            raise ValidationError('Please use a different username.')

    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user is not None:
            raise ValidationError('Please use a different email address.')


class EditProfileForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    group = SelectField("Choose your Company: ", choices=[('blue', 'Blue Squares'),
                                                          ('red', 'Red Dragons'),
                                                          ('green', 'Green Scales'),
                                                          ('prple', 'Purple Royals')], default='blue')
    submit = SubmitField('Submit')

    def __init__(self, original_username, original_group, *args, **kwargs):
        super(EditProfileForm, self).__init__(*args, **kwargs)
        self.original_username = original_username
        self.original_group = original_group

    def validate_username(self, username):
        if username.data != self.original_username:
            user = User.query.filter_by(username=self.username.data).first()
            if user is not None:
                raise ValidationError('Please use a different username.')

    def validate_group(self, group):
        if group.data != self.original_group:
            user = User.query.filter_by(group=self.group.data).first()


class DeedForm(FlaskForm):
    title = StringField('Title', validators=[
        DataRequired(), Length(min=1, max=25)])
    body = TextAreaField('Say something', validators=[
        DataRequired(), Length(min=1, max=140)])
    submit = SubmitField('Submit')
