"""
ResumeIQ - AI Resume Analyzer & Career Guidance Portal
Main Flask Application
"""
import os
import json
import uuid
from datetime import datetime
from functools import wraps

from flask import (Flask, render_template, request, redirect, url_for,
                   flash, session, send_file, jsonify, abort)
from flask_login import (LoginManager, login_user, logout_user,
                         login_required, current_user)
from werkzeug.utils import secure_filename

from config import Config
from models.models import db, User, Resume, Skill
from utils.resume_parser import extract_text
from utils.analyzer import analyze_resume
from utils.skill_detector import detect_skills
from utils.job_predictor import predict_jobs
from utils.interview_questions import generate_questions
from utils.career_roadmap import get_roadmap, get_all_roles, get_role_summary
from utils.chatbot import get_chatbot_response

# ─── App Initialization ────────────────────────────────────────────────────────
app = Flask(__name__)
app.config.from_object(Config)

# Ensure required directories exist
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)
os.makedirs(os.path.join(os.path.dirname(__file__), 'database'), exist_ok=True)

# Initialize extensions
db.init_app(app)
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'
login_manager.login_message_category = 'info'


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


def admin_required(f):
    """Decorator to restrict routes to admin users only."""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not current_user.is_authenticated or current_user.role != 'admin':
            flash('Access denied. Admin privileges required.', 'danger')
            return redirect(url_for('dashboard'))
        return f(*args, **kwargs)
    return decorated_function


def allowed_file(filename):
    """Check if the uploaded file has an allowed extension."""
    return '.' in filename and \
        filename.rsplit('.', 1)[1].lower() in app.config['ALLOWED_EXTENSIONS']


# ─── Create Database Tables ────────────────────────────────────────────────────
with app.app_context():
    db.create_all()
    # Create default admin user if not exists
    admin = User.query.filter_by(email='admin@resumeiq.com').first()
    if not admin:
        admin = User(name='Admin', email='admin@resumeiq.com', role='admin')
        admin.set_password('admin123')
        db.session.add(admin)
        db.session.commit()


# ─── Public Routes ─────────────────────────────────────────────────────────────

@app.route('/')
def index():
    """Landing page."""
    return render_template('index.html')


@app.route('/login', methods=['GET', 'POST'])
def login():
    """User login page."""
    if current_user.is_authenticated:
        return redirect(url_for('dashboard'))

    if request.method == 'POST':
        email = request.form.get('email', '').strip()
        password = request.form.get('password', '')

        if not email or not password:
            flash('Please fill in all fields.', 'danger')
            return render_template('login.html')

        user = User.query.filter_by(email=email).first()
        if user and user.check_password(password):
            login_user(user)
            flash(f'Welcome back, {user.name}!', 'success')
            next_page = request.args.get('next')
            if user.role == 'admin':
                return redirect(next_page or url_for('admin_dashboard'))
            return redirect(next_page or url_for('dashboard'))
        else:
            flash('Invalid email or password.', 'danger')

    return render_template('login.html')


@app.route('/signup', methods=['GET', 'POST'])
def signup():
    """User registration page."""
    if current_user.is_authenticated:
        return redirect(url_for('dashboard'))

    if request.method == 'POST':
        name = request.form.get('name', '').strip()
        email = request.form.get('email', '').strip()
        password = request.form.get('password', '')
        confirm_password = request.form.get('confirm_password', '')

        # Validation
        if not all([name, email, password, confirm_password]):
            flash('Please fill in all fields.', 'danger')
            return render_template('signup.html')

        if password != confirm_password:
            flash('Passwords do not match.', 'danger')
            return render_template('signup.html')

        if len(password) < 6:
            flash('Password must be at least 6 characters.', 'danger')
            return render_template('signup.html')

        if User.query.filter_by(email=email).first():
            flash('Email already registered.', 'danger')
            return render_template('signup.html')

        # Create new user
        user = User(name=name, email=email, role='user')
        user.set_password(password)
        db.session.add(user)
        db.session.commit()

        flash('Account created successfully! Please log in.', 'success')
        return redirect(url_for('login'))

    return render_template('signup.html')


@app.route('/logout')
@login_required
def logout():
    """Log out the current user."""
    logout_user()
    flash('You have been logged out.', 'info')
    return redirect(url_for('index'))


@app.route('/contact', methods=['GET', 'POST'])
def contact():
    """Contact page."""
    if request.method == 'POST':
        flash('Thank you for your message! We\'ll get back to you soon.', 'success')
        return redirect(url_for('contact'))
    return render_template('contact.html')


# ─── User Dashboard Routes ─────────────────────────────────────────────────────

@app.route('/dashboard')
@login_required
def dashboard():
    """User dashboard showing uploaded resumes and analytics."""
    resumes = Resume.query.filter_by(user_id=current_user.id)\
        .order_by(Resume.upload_date.desc()).all()
    return render_template('dashboard.html', resumes=resumes)


@app.route('/upload', methods=['GET', 'POST'])
@login_required
def upload():
    """Resume upload page with drag-and-drop support."""
    if request.method == 'POST':
        if 'resume' not in request.files:
            flash('No file selected.', 'danger')
            return redirect(url_for('upload'))

        file = request.files['resume']
        if file.filename == '':
            flash('No file selected.', 'danger')
            return redirect(url_for('upload'))

        if not allowed_file(file.filename):
            flash('Invalid file type. Only PDF and DOCX files are accepted.', 'danger')
            return redirect(url_for('upload'))

        # Save file with unique name
        original_filename = secure_filename(file.filename)
        unique_filename = f"{uuid.uuid4().hex}_{original_filename}"
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], unique_filename)
        file.save(filepath)

        # Extract text from resume
        extracted_text = extract_text(filepath)
        if not extracted_text:
            flash('Could not extract text from the uploaded file. Please try another file.', 'warning')
            os.remove(filepath)
            return redirect(url_for('upload'))

        # Detect skills
        skill_results = detect_skills(extracted_text)

        # Analyze resume
        analysis = analyze_resume(extracted_text, skill_results['found'])

        # Predict job roles
        job_matches = predict_jobs(skill_results['found'])

        # Generate interview questions
        questions = generate_questions(skill_results['found'])

        # Store analysis data as JSON
        analysis_json = json.dumps({
            'analysis': analysis,
            'skills': skill_results,
            'jobs': job_matches,
            'questions': questions
        })

        # Save to database
        resume = Resume(
            user_id=current_user.id,
            filename=unique_filename,
            original_filename=original_filename,
            extracted_text=extracted_text,
            score=analysis['resume_score'],
            ats_score=analysis['ats_score'],
            analysis_data=analysis_json
        )
        db.session.add(resume)
        db.session.flush()  # Get the resume ID

        # Save detected skills
        for skill_name in skill_results['found']:
            # Find category
            category = 'Other'
            for cat, skills_list in skill_results['by_category'].items():
                if skill_name in skills_list:
                    category = cat
                    break
            skill = Skill(resume_id=resume.id, skill_name=skill_name, category=category)
            db.session.add(skill)

        db.session.commit()

        flash('Resume uploaded and analyzed successfully!', 'success')
        return redirect(url_for('analysis', resume_id=resume.id))

    # GET - show upload page with history
    resumes = Resume.query.filter_by(user_id=current_user.id)\
        .order_by(Resume.upload_date.desc()).all()
    return render_template('upload.html', resumes=resumes)


@app.route('/analysis/<int:resume_id>')
@login_required
def analysis(resume_id):
    """Display resume analysis results."""
    resume = Resume.query.get_or_404(resume_id)

    # Security check - only owner or admin can view
    if resume.user_id != current_user.id and current_user.role != 'admin':
        abort(403)

    # Parse analysis data
    analysis_data = json.loads(resume.analysis_data) if resume.analysis_data else {}

    return render_template('analysis.html',
                           resume=resume,
                           analysis=analysis_data.get('analysis', {}),
                           skills=analysis_data.get('skills', {}),
                           jobs=analysis_data.get('jobs', []),
                           questions=analysis_data.get('questions', {}))


@app.route('/career-roadmap')
@login_required
def career_roadmap():
    """Career roadmap selection and display page."""
    selected_role = request.args.get('role', '')
    roadmap = None
    if selected_role:
        roadmap = get_roadmap(selected_role)

    roles = get_role_summary()
    return render_template('career_roadmap.html',
                           roles=roles,
                           selected_role=selected_role,
                           roadmap=roadmap)


@app.route('/delete-resume/<int:resume_id>', methods=['POST'])
@login_required
def delete_resume(resume_id):
    """Delete a user's own resume."""
    resume = Resume.query.get_or_404(resume_id)
    if resume.user_id != current_user.id and current_user.role != 'admin':
        abort(403)

    # Delete file from disk
    filepath = os.path.join(app.config['UPLOAD_FOLDER'], resume.filename)
    if os.path.exists(filepath):
        os.remove(filepath)

    db.session.delete(resume)
    db.session.commit()
    flash('Resume deleted successfully.', 'success')

    if current_user.role == 'admin':
        return redirect(url_for('admin_dashboard'))
    return redirect(url_for('dashboard'))


# ─── API Routes ─────────────────────────────────────────────────────────────────

@app.route('/api/analysis-data/<int:resume_id>')
@login_required
def api_analysis_data(resume_id):
    """API endpoint returning analysis data for charts."""
    resume = Resume.query.get_or_404(resume_id)
    if resume.user_id != current_user.id and current_user.role != 'admin':
        abort(403)

    analysis_data = json.loads(resume.analysis_data) if resume.analysis_data else {}
    return jsonify(analysis_data)


@app.route('/api/chat', methods=['POST'])
def api_chat():
    """Chatbot API endpoint."""
    data = request.get_json()
    message = data.get('message', '') if data else ''
    response = get_chatbot_response(message)
    return jsonify({'response': response})


@app.route('/download-report/<int:resume_id>')
@login_required
def download_report(resume_id):
    """Download analysis report as PDF."""
    resume = Resume.query.get_or_404(resume_id)
    if resume.user_id != current_user.id and current_user.role != 'admin':
        abort(403)

    analysis_data = json.loads(resume.analysis_data) if resume.analysis_data else {}

    # Generate PDF report
    from utils.report_generator import generate_pdf_report
    pdf_path = generate_pdf_report(resume, analysis_data)

    return send_file(pdf_path, as_attachment=True,
                     download_name=f'ResumeIQ_Report_{resume.original_filename}.pdf')


# ─── Admin Routes ──────────────────────────────────────────────────────────────

@app.route('/admin')
@login_required
@admin_required
def admin_dashboard():
    """Admin dashboard with analytics and user management."""
    users = User.query.all()
    resumes = Resume.query.order_by(Resume.upload_date.desc()).all()

    # Analytics
    total_users = User.query.count()
    total_resumes = Resume.query.count()
    avg_score = db.session.query(db.func.avg(Resume.score)).scalar() or 0
    avg_ats = db.session.query(db.func.avg(Resume.ats_score)).scalar() or 0

    # Recent activity
    recent_resumes = Resume.query.order_by(Resume.upload_date.desc()).limit(10).all()

    return render_template('admin.html',
                           users=users,
                           resumes=resumes,
                           total_users=total_users,
                           total_resumes=total_resumes,
                           avg_score=round(avg_score, 1),
                           avg_ats=round(avg_ats, 1),
                           recent_resumes=recent_resumes)


@app.route('/admin/delete-user/<int:user_id>', methods=['POST'])
@login_required
@admin_required
def admin_delete_user(user_id):
    """Admin: Delete a user and their data."""
    user = User.query.get_or_404(user_id)
    if user.role == 'admin':
        flash('Cannot delete admin users.', 'danger')
        return redirect(url_for('admin_dashboard'))

    # Delete user's uploaded files
    for resume in user.resumes:
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], resume.filename)
        if os.path.exists(filepath):
            os.remove(filepath)

    db.session.delete(user)
    db.session.commit()
    flash(f'User {user.name} has been deleted.', 'success')
    return redirect(url_for('admin_dashboard'))


# ─── Error Handlers ─────────────────────────────────────────────────────────────

@app.errorhandler(404)
def not_found(e):
    return render_template('base.html', error='Page not found'), 404


@app.errorhandler(403)
def forbidden(e):
    return render_template('base.html', error='Access denied'), 403


@app.errorhandler(413)
def too_large(e):
    flash('File is too large. Maximum size is 16MB.', 'danger')
    return redirect(url_for('upload'))


# ─── Run Application ───────────────────────────────────────────────────────────

import os

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)
