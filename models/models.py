"""
ResumeIQ Database Models
Defines User, Resume, and Skill tables using Flask-SQLAlchemy.
"""
from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash

db = SQLAlchemy()


class User(UserMixin, db.Model):
    """User model with authentication and role support."""
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(256), nullable=False)
    role = db.Column(db.String(20), default='user')  # 'user' or 'admin'
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    resumes = db.relationship('Resume', backref='user', lazy=True, cascade='all, delete-orphan')

    def set_password(self, password):
        self.password = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password, password)

    def __repr__(self):
        return f'<User {self.name}>'


class Resume(db.Model):
    """Resume model storing uploaded file metadata and analysis results."""
    __tablename__ = 'resumes'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    filename = db.Column(db.String(255), nullable=False)
    original_filename = db.Column(db.String(255), nullable=False)
    extracted_text = db.Column(db.Text)
    score = db.Column(db.Float, default=0)
    ats_score = db.Column(db.Float, default=0)
    analysis_data = db.Column(db.Text)  # JSON-encoded analysis results
    upload_date = db.Column(db.DateTime, default=datetime.utcnow)

    skills = db.relationship('Skill', backref='resume', lazy=True, cascade='all, delete-orphan')

    def __repr__(self):
        return f'<Resume {self.original_filename}>'


class Skill(db.Model):
    """Skill model linking detected skills to resumes."""
    __tablename__ = 'skills'

    id = db.Column(db.Integer, primary_key=True)
    resume_id = db.Column(db.Integer, db.ForeignKey('resumes.id'), nullable=False)
    skill_name = db.Column(db.String(100), nullable=False)
    category = db.Column(db.String(50))

    def __repr__(self):
        return f'<Skill {self.skill_name}>'
