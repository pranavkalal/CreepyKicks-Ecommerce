from flask_wtf import FlaskForm
from wtforms.fields import SubmitField, StringField
from wtforms.validators import InputRequired, Email

# form used in basket
class CheckoutForm(FlaskForm):
    first_name = StringField("First Name", validators=[InputRequired()])
    surname = StringField("Last Name", validators=[InputRequired()])
    email = StringField("Email", validators=[InputRequired(), Email()])
    phone = StringField("Phone Number", validators=[InputRequired()])
    address = StringField("Address", validators=[InputRequired()])
    submit = SubmitField("Place Order")