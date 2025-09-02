from flask_wtf import FlaskForm

from wtforms import StringField, SubmitField, PasswordField

from wtforms.validators import DataRequired, Length


class AddClientForm(FlaskForm):
    first_name = StringField("Enter Clients first name", validators=[DataRequired(), Length(min=2, max=25)])
    last_name = StringField("Enter Clients last name", validators=[DataRequired(), Length(min=2, max=25)])
    phone_number = StringField("Enter Clients phone number", validators=[DataRequired(), Length(min=2, max=25)])
    notes = StringField("notes: ", validators=[Length(min=2, max=25)])

    submit = SubmitField("Submit")


class AddTattoo(FlaskForm):
    title = StringField("Enter title for tattoo", validators=[DataRequired(), Length(min=2, max=25)])
    note = StringField("notes: ", validators=[Length(min=0, max=300)])

    submit = SubmitField("Submit")
