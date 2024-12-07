from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin
from datetime import datetime

# Инициализация базы данных
db = SQLAlchemy()

# Модель роли
class Role(db.Model):
    __tablename__ = 'roles'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), unique=True, nullable=False)
    description = db.Column(db.String(255), nullable=True)
    users = db.relationship('User', backref='role', lazy=True)

    def __repr__(self):
        return f"<Role {self.name}>"

# Модель пользователя
class User(db.Model, UserMixin):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True, nullable=False)
    password_hash = db.Column(db.String(128), nullable=False)
    role_id = db.Column(db.Integer, db.ForeignKey('roles.id'), nullable=False)
    logs = db.relationship('Log', backref='user', lazy=True)

    def __repr__(self):
        return f"<User {self.username}>"

# Модель логов
class Log(db.Model):
    __tablename__ = 'logs'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    category = db.Column(db.String(50), nullable=False)
    action = db.Column(db.String(255), nullable=False)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    details = db.Column(db.Text, nullable=True)

    def __repr__(self):
        return f"<Log User:{self.user_id} Action:{self.action}>"

# Модель мест
class Place(db.Model):
    __tablename__ = 'places'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text, nullable=True)
    category = db.Column(db.String(50), nullable=True)
    rating = db.Column(db.Float, default=0.0)
    geographical_location = db.Column(db.String(100), nullable=True)
    routes = db.relationship('Route', backref='place', lazy=True)

    def __repr__(self):
        return f"<Place {self.name}>"

# Модель маршрутов
class Route(db.Model):
    __tablename__ = 'routes'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    creation_date = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    duration = db.Column(db.Interval, nullable=True)
    difficulty = db.Column(db.Integer, default=1)
    age_restrictions = db.Column(db.Integer, nullable=True)
    place_id = db.Column(db.Integer, db.ForeignKey('places.id'), nullable=True)
    comments = db.relationship('Comment', backref='route', lazy=True)

    def __repr__(self):
        return f"<Route {self.name}>"

# Модель комментариев
class Comment(db.Model):
    __tablename__ = 'comments'
    id = db.Column(db.Integer, primary_key=True)
    message = db.Column(db.Text, nullable=False)
    date_created = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    route_id = db.Column(db.Integer, db.ForeignKey('routes.id'), nullable=True)

    def __repr__(self):
        return f"<Comment User:{self.user_id} Route:{self.route_id}>"
