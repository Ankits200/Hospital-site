from flask_wtf import FlaskForm
from wtforms.fields import StringField, PasswordField, SubmitField,IntegerField,DateField
from wtforms.validators import DataRequired, Length
from config import Config

class MyForm(FlaskForm):
    username = StringField(label='Username', validators=[DataRequired()])
    password = PasswordField(label='Password', validators=[DataRequired(), Length(8,30,"Please enter at least 8 characters")])
    submit = SubmitField(label='Login')

class addForm(FlaskForm):
    name = StringField(label="Patient name",validators=[DataRequired()])
    address = StringField(label="Address",validators=[DataRequired()])
    contact = StringField(label="Contact no.",validators=[DataRequired()])
    age = IntegerField(label="Age",validators=[DataRequired()])
    date = DateField(label="Date",validators=[DataRequired()])
    UHID = StringField(label="Unique UHID",validators=[DataRequired()])
    opd = StringField(label="OPD",validators=[DataRequired()])
    consultantName = StringField(label="Consultant Name",validators=[DataRequired()])
    add = SubmitField(label="ADD")

class searchForm(FlaskForm):
    UHID = StringField(label="Enter UHID to search", validators=[DataRequired()])
    search = SubmitField(label='Search')