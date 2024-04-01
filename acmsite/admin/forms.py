from flask_wtf import FlaskForm
from wtforms import DateTimeField, DateField, SelectField, StringField, TextAreaField, TimeField
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

class OfficerForm(FlaskForm):
    position = SelectField("Position", choices=["President", "Vice President",
                                                "Treasurer", "Secretary", "PR Chair", "Hackathon Manager 1",
                                                "Hackathon Manager 2", "System Administrator"],
                           validators=[DataRequired()])
    term_start = DateField("Term Start", validators=[DataRequired()])
    term_end = DateField("Term End", validators=[DataRequired()]) 
