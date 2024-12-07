from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, SelectField, TextAreaField, IntegerField, DateField
from wtforms.validators import DataRequired, Length, EqualTo, ValidationError
from models import User

# Форма авторизации
class LoginForm(FlaskForm):
    username = StringField("Username", validators=[DataRequired(), Length(min=4, max=50)])
    password = PasswordField("Password", validators=[DataRequired()])
    submit = SubmitField("Login")

# Форма регистрации
class RegisterForm(FlaskForm):
    username = StringField("Username", validators=[DataRequired(), Length(min=4, max=50)])
    password = PasswordField("Password", validators=[DataRequired(), Length(min=6)])
    confirm_password = PasswordField("Confirm Password", validators=[
        DataRequired(), EqualTo('password', message="Passwords must match")
    ])
    role = SelectField("Role", coerce=int, validators=[DataRequired()])
    submit = SubmitField("Register")

    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        if user:
            raise ValidationError("Username already exists. Please choose a different one.")

# Форма добавления и редактирования маршрутов
class RouteForm(FlaskForm):
    name = StringField("Route Name", validators=[DataRequired(), Length(max=100)])
    duration = StringField("Duration (e.g., 2:30:00)", validators=[DataRequired()])
    difficulty = IntegerField("Difficulty (1-5)", validators=[DataRequired()])
    age_restrictions = IntegerField("Age Restrictions", validators=[])
    place_id = IntegerField("Place ID", validators=[])
    submit = SubmitField("Save Route")

# Форма добавления и редактирования мест
class PlaceForm(FlaskForm):
    name = StringField("Place Name", validators=[DataRequired(), Length(max=100)])
    description = TextAreaField("Description", validators=[DataRequired()])
    category = StringField("Category", validators=[Length(max=50)])
    rating = IntegerField("Rating (1-5)", validators=[])
    geographical_location = StringField("Geographical Location", validators=[Length(max=100)])
    submit = SubmitField("Save Place")

# Форма добавления комментариев
class CommentForm(FlaskForm):
    message = TextAreaField("Comment", validators=[DataRequired(), Length(max=500)])
    route_id = IntegerField("Route ID", validators=[DataRequired()])
    submit = SubmitField("Submit Comment")

# Форма фильтрации логов
class FilterLogsForm(FlaskForm):
    user_id = IntegerField("User ID", validators=[])
    category = SelectField("Category", choices=[
        ("", "All"),
        ("content_update", "Content Update"),
        ("user_management", "User Management"),
        ("security", "Security"),
    ], validators=[])
    start_date = DateField("Start Date", format='%Y-%m-%d', validators=[])
    end_date = DateField("End Date", format='%Y-%m-%d', validators=[])
    submit = SubmitField("Filter Logs")
