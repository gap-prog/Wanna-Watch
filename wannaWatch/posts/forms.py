from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, RadioField, HiddenField
from wtforms.validators import DataRequired


class GetTitle(FlaskForm):
	title = StringField("Title", validators=[DataRequired()])
	submit = SubmitField("Get")


class GetParticipants(FlaskForm):
    participants = StringField("Participants (username separated by comma)", validators=[DataRequired()])
    submit = SubmitField("Submit")


class SearchTitle(FlaskForm):
    title = StringField("Search movie or TV show title", validators=[DataRequired()])
    submit = SubmitField("Search")


class PickTime(FlaskForm):
    values = RadioField("Options", choices=["Immediately", "Later", "Never"], validators=[DataRequired()])
    post_id = ""
    submit_name = ""
    submit = SubmitField(submit_name)
