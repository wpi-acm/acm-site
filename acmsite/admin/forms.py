from flask_wtf import FlaskForm
from wtforms import DateTimeField, DateField, StringField, TextAreaField, TimeField
from wtforms.validators import DataRequired

class EventForm(FlaskForm):
    name = StringField('Name', validators=[DataRequired()])
    description = TextAreaField('Description')
    location = StringField('Location', validators=[DataRequired()])
    start_day = DateField('Start Day', validators=[DataRequired()])
    start_time = TimeField('Start Time')
    end_day = DateField('End Day', validators=[DataRequired()])
    end_time = TimeField('End Time')

class LinkForm(FlaskForm):
    slug = StringField("Slug", validators=[DataRequired()])
    destination = StringField("Destination", validators=[DataRequired()])
