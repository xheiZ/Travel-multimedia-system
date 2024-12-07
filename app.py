from flask import Flask, render_template, request, redirect, url_for, jsonify, flash
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager, login_user, logout_user, login_required, current_user
from werkzeug.security import generate_password_hash, check_password_hash
from config import Config
from models import db, User, Role, Log, Route, Place
from forms import LoginForm, RegisterForm
from utils import log_action, role_required

# Инициализация приложения
app = Flask(__name__)
app.config.from_object(Config)

# Инициализация базы данных и миграций
db.init_app(app)
migrate = Migrate(app, db)

# Настройка Flask-Login
login_manager = LoginManager(app)
login_manager.login_view = "login"

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

# Главная страница
@app.route("/")
def index():
    return render_template("index.html", title="Welcome")

# Авторизация
@app.route("/login", methods=["GET", "POST"])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user and check_password_hash(user.password_hash, form.password.data):
            login_user(user)
            flash("Logged in successfully.", "success")
            return redirect(url_for("dashboard"))
        else:
            flash("Invalid username or password.", "danger")
    return render_template("login.html", form=form, title="Login")

# Регистрация
@app.route("/register", methods=["GET", "POST"])
def register():
    form = RegisterForm()
    roles = Role.query.all()
    if form.validate_on_submit():
        existing_user = User.query.filter_by(username=form.username.data).first()
        if existing_user:
            flash("Username already exists.", "danger")
        else:
            hashed_password = generate_password_hash(form.password.data)
            new_user = User(
                username=form.username.data,
                password_hash=hashed_password,
                role_id=form.role.data
            )
            db.session.add(new_user)
            db.session.commit()
            flash("Registration successful. Please log in.", "success")
            return redirect(url_for("login"))
    return render_template("register.html", form=form, roles=roles, title="Register")

# Главная панель для разных ролей
@app.route("/dashboard")
@login_required
def dashboard():
    if current_user.role.name == "superadmin":
        return render_template("roles/superadmin.html", title="Superadmin Dashboard")
    elif current_user.role.name == "content_admin":
        return render_template("roles/content_admin.html", title="Content Admin Dashboard")
    elif current_user.role.name == "user_admin":
        return render_template("roles/user_admin.html", title="User Admin Dashboard")
    elif current_user.role.name == "auditor":
        return render_template("roles/auditor.html", title="Auditor Dashboard")
    else:
        return render_template("dashboard_user.html", title="User Dashboard")

# Логи
@app.route("/logs", methods=["GET"])
@login_required
@role_required("superadmin", "auditor")
def logs():
    logs = Log.query.all()
    return render_template("logs.html", logs=logs, title="Logs")

@app.route("/logs/filter", methods=["GET", "POST"])
@login_required
@role_required("superadmin", "auditor")
def filter_logs():
    logs = []
    if request.method == "POST":
        user_id = request.form.get("user_id")
        category = request.form.get("category")
        start_date = request.form.get("start_date")
        end_date = request.form.get("end_date")

        query = Log.query
        if user_id:
            query = query.filter_by(user_id=user_id)
        if category:
            query = query.filter_by(category=category)
        if start_date and end_date:
            query = query.filter(Log.timestamp.between(start_date, end_date))
        logs = query.all()

    return render_template("filter_logs.html", logs=logs, title="Filter Logs")

# Управление пользователями (для суперадминистратора и администратора пользователей)
@app.route("/manage_users", methods=["GET", "POST"])
@login_required
@role_required("superadmin", "user_admin")
def manage_users():
    users = User.query.all()
    return render_template("manage_users.html", users=users, title="Manage Users")

# Управление контентом (для контент-администратора)
@app.route("/manage_routes", methods=["GET", "POST"])
@login_required
@role_required("content_admin")
def manage_routes():
    routes = Route.query.all()
    return render_template("manage_routes.html", routes=routes, title="Manage Routes")

@app.route("/manage_places", methods=["GET", "POST"])
@login_required
@role_required("content_admin")
def manage_places():
    places = Place.query.all()
    return render_template("manage_places.html", places=places, title="Manage Places")

# Выход из системы
@app.route("/logout")
@login_required
def logout():
    logout_user()
    flash("Logged out successfully.", "info")
    return redirect(url_for("index"))

# Обработчик ошибок
@app.errorhandler(403)
def access_denied(e):
    return render_template("403.html", title="Access Denied"), 403

@app.errorhandler(404)
def page_not_found(e):
    return render_template("404.html", title="Page Not Found"), 404

# Запуск приложения
if __name__ == "__main__":
    with app.app_context():
        db.create_all()
    app.run(debug=True)
