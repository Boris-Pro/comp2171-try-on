from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, FloatField, TextAreaField, IntegerField, SelectField, SubmitField,DateField, TimeField
from wtforms.validators import InputRequired, DataRequired, NumberRange
from flask_wtf.file import FileField, FileAllowed, FileRequired


class LoginForm(FlaskForm):
    user_name = StringField('Username', validators=[InputRequired()])
    password = PasswordField('Password', validators=[InputRequired()])


class RegisterForm(FlaskForm):
    first_name = StringField('First Name', validators=[InputRequired()])
    last_name = StringField('Last Name', validators=[InputRequired()])
    user_name = StringField('User Name', validators=[InputRequired()])
    email = StringField('Email', validators=[InputRequired()])
    user_type = SelectField('User Type', choices=[('buyer', 'Buyer'), ('seller', 'Seller')], validators=[DataRequired()])
    password = PasswordField('Password', validators=[InputRequired()])

class ProductForm(FlaskForm):
    name = StringField('Name', validators=[DataRequired()])
    price = FloatField('Price', validators=[DataRequired()])
    description = TextAreaField('Description', validators=[InputRequired()])
    quantity = IntegerField('Quantity', validators=[InputRequired()])
    category = StringField('Category', validators=[InputRequired()])
    weight = FloatField('Weight', validators=[InputRequired()])
    image = FileField('Image File', validators=[FileRequired(), FileAllowed(['jpg', 'png'], 'Images only!')])

class ReviewForm(FlaskForm):
    rating = IntegerField('Rating', validators=[DataRequired(), NumberRange(min=1, max=5)])
    comment = TextAreaField('Comment')
    submit = SubmitField('Submit Review')



class AppointmentForm(FlaskForm):
    date = DateField('Date', validators=[DataRequired()])
    time = TimeField('Time', validators=[DataRequired()])
    #location = StringField('Location', validators=[DataRequired()])
    purpose = StringField('Purpose', validators=[DataRequired()])
    items_to_view = StringField('Items to View')
    notes = TextAreaField('Notes')
    # product_id = SelectField('Product', coerce=int)