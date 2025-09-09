from flask_wtf import FlaskForm

from wtforms import StringField, SubmitField, HiddenField, IntegerField, DateField, TimeField, SelectField

from wtforms.validators import DataRequired, Length, Optional


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


class EditTattoo(FlaskForm):
    title = StringField("Enter title for tattoo", validators=[Length(min=0, max=25), Optional()])
    price_estimate = IntegerField("Price Estimation", validators=[Optional()])
    price_final = IntegerField("Final Price", validators=[Optional()])
    status = StringField("Status", validators=[Length(min=0, max=30), Optional()])
    note = StringField("notes: ", validators=[Length(min=0, max=300), Optional()])

    submit = SubmitField("Submit")


class BookingForm(FlaskForm):
    date = DateField("Enter date")
    start_time = TimeField("Start time")
    end_time = TimeField("End time")
    booking_type = SelectField("What type of booking is it?",
                               choices=[("Consultation", "Consultation"), ("Inking", "Inking")])

    submit = SubmitField("Submit")


class PaymentForm(FlaskForm):
    amount = IntegerField("Amount")
    payment_type = SelectField("Payment method",
                               choices=[("Cash", "Cash"), ("Bank Transfer", "Bank Transfer")])
    notes = SelectField("Session Type",
                        choices=[("Inking", "Inking"), ("Deposit", "Deposit")])
    date = DateField("Paid On")
    booking_id = HiddenField(validators=[DataRequired()])

    submit = SubmitField("Submit")
