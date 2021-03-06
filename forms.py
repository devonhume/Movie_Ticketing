from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, PasswordField, IntegerField, BooleanField, SelectField
from wtforms.validators import DataRequired, URL, Email


class TicketsForm(FlaskForm):
    adult_tickets = IntegerField("Adult Tickets (13 and up)", validators=[DataRequired()])
    child_tickets = IntegerField("Child Tickets (12 and under)", validators=[DataRequired()])
    submit = SubmitField("Buy")


class PurchaseForm(FlaskForm):
    first_name = StringField("First Name", validators=[DataRequired()])
    last_name = StringField("Last Name", validators=[DataRequired()])
    email = StringField("Email", validators=[Email(), DataRequired()])
    credit_card = IntegerField("Credit Card", validators=[DataRequired()])
    exp_month = IntegerField("Expiration Month", validators=[DataRequired()])
    exp_year = IntegerField("Expiration Year", validators=[DataRequired()])
    secret_code = IntegerField("Secret Code", validators=[DataRequired()])
    purchase_submit = SubmitField("Purchase")

class ConfirmForm(FlaskForm):
    confirm = SubmitField("Close")