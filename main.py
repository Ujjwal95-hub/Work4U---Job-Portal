from flask import Flask, render_template, redirect, url_for, request, flash
from flask_login import LoginManager, login_user, logout_user, login_required, current_user
from werkzeug.security import generate_password_hash, check_password_hash
from models import db, User, Job, Application

app = Flask(__name__)
app.config['SECRET_KEY'] = 'work4u_secret_key_2024'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///work4u.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)
login_manager = LoginManager(app)
login_manager.login_view = 'login'


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


# ── Create DB & Admin ──────────────────────────────────────────
with app.app_context():
    db.create_all()
    if not User.query.filter_by(email='admin@work4u.com').first():
        admin = User(
            name='Admin',
            email='admin@work4u.com',
            password=generate_password_hash('admin123'),
            role='admin'
        )
        db.session.add(admin)
        db.session.commit()
        print("✅ Admin created: admin@work4u.com / admin123")


# ── Home ───────────────────────────────────────────────────────
@app.route('/')
def index():
    jobs = Job.query.order_by(Job.created_at.desc()).limit(6).all()
    return render_template('index.html', jobs=jobs)


# ── Register ───────────────────────────────────────────────────
@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        name = request.form.get('name')
        email = request.form.get('email')
        password = request.form.get('password')
        role = request.form.get('role')

        if User.query.filter_by(email=email).first():
            flash('Email already registered!', 'danger')
            return redirect(url_for('register'))

        user = User(
            name=name,
            email=email,
            password=generate_password_hash(password),
            role=role
        )
        db.session.add(user)
        db.session.commit()
        flash('Account created! Please login.', 'success')
        return redirect(url_for('login'))

    return render_template('register.html')


# ── Login ──────────────────────────────────────────────────────
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')
        user = User.query.filter_by(email=email).first()

        if user and check_password_hash(user.password, password):
            login_user(user)
            flash(f'Welcome back, {user.name}!', 'success')
            if user.role == 'admin':
                return redirect(url_for('admin_panel'))
            elif user.role == 'employer':
                return redirect(url_for('employer_dashboard'))
            else:
                return redirect(url_for('seeker_dashboard'))
        else:
            flash('Invalid email or password!', 'danger')

    return render_template('login.html')


# ── Logout ─────────────────────────────────────────────────────
@app.route('/logout')
@login_required
def logout():
    logout_user()
    flash('Logged out successfully!', 'success')
    return redirect(url_for('index'))


# ── Jobs Listing ───────────────────────────────────────────────
@app.route('/jobs')
def jobs():
    search = request.args.get('search', '')
    location = request.args.get('location', '')
    category = request.args.get('category', '')

    query = Job.query
    if search:
        query = query.filter(Job.title.ilike(f'%{search}%') | Job.company.ilike(f'%{search}%'))
    if location:
        query = query.filter(Job.location.ilike(f'%{location}%'))
    if category:
        query = query.filter(Job.category.ilike(f'%{category}%'))

    jobs = query.order_by(Job.created_at.desc()).all()
    return render_template('jobs.html', jobs=jobs, search=search, location=location, category=category)


# ── Job Detail ─────────────────────────────────────────────────
@app.route('/job/<int:job_id>')
def job_detail(job_id):
    job = Job.query.get_or_404(job_id)
    already_applied = False
    if current_user.is_authenticated and current_user.role == 'jobseeker':
        already_applied = Application.query.filter_by(
            job_id=job_id, seeker_id=current_user.id).first() is not None
    return render_template('job_detail.html', job=job, already_applied=already_applied)


# ── Apply for Job ──────────────────────────────────────────────
@app.route('/apply/<int:job_id>')
@login_required
def apply_job(job_id):
    if current_user.role != 'jobseeker':
        flash('Only job seekers can apply!', 'danger')
        return redirect(url_for('job_detail', job_id=job_id))

    already = Application.query.filter_by(job_id=job_id, seeker_id=current_user.id).first()
    if already:
        flash('You have already applied for this job!', 'warning')
        return redirect(url_for('job_detail', job_id=job_id))

    application = Application(job_id=job_id, seeker_id=current_user.id)
    db.session.add(application)
    db.session.commit()
    flash('Application submitted successfully!', 'success')
    return redirect(url_for('seeker_dashboard'))


# ── Seeker Dashboard ───────────────────────────────────────────
@app.route('/dashboard/seeker')
@login_required
def seeker_dashboard():
    if current_user.role != 'jobseeker':
        return redirect(url_for('index'))
    applications = Application.query.filter_by(seeker_id=current_user.id).all()
    return render_template('seeker_dashboard.html', applications=applications)


# ── Employer Dashboard ─────────────────────────────────────────
@app.route('/dashboard/employer')
@login_required
def employer_dashboard():
    if current_user.role != 'employer':
        return redirect(url_for('index'))
    jobs = Job.query.filter_by(employer_id=current_user.id).all()
    return render_template('employer_dashboard.html', jobs=jobs)


# ── Post Job ───────────────────────────────────────────────────
@app.route('/post-job', methods=['GET', 'POST'])
@login_required
def post_job():
    if current_user.role != 'employer':
        flash('Only employers can post jobs!', 'danger')
        return redirect(url_for('index'))

    if request.method == 'POST':
        job = Job(
            title=request.form.get('title'),
            description=request.form.get('description'),
            salary=request.form.get('salary'),
            location=request.form.get('location'),
            category=request.form.get('category'),
            company=request.form.get('company'),
            employer_id=current_user.id
        )
        db.session.add(job)
        db.session.commit()
        flash('Job posted successfully!', 'success')
        return redirect(url_for('employer_dashboard'))

    return render_template('post_job.html')


# ── Delete Job ─────────────────────────────────────────────────
@app.route('/delete-job/<int:job_id>')
@login_required
def delete_job(job_id):
    job = Job.query.get_or_404(job_id)
    if job.employer_id != current_user.id and current_user.role != 'admin':
        flash('Unauthorized!', 'danger')
        return redirect(url_for('index'))
    Application.query.filter_by(job_id=job_id).delete()
    db.session.delete(job)
    db.session.commit()
    flash('Job deleted!', 'success')
    return redirect(url_for('employer_dashboard'))


# ── Admin Panel ────────────────────────────────────────────────
@app.route('/admin')
@login_required
def admin_panel():
    if current_user.role != 'admin':
        flash('Unauthorized!', 'danger')
        return redirect(url_for('index'))
    users = User.query.all()
    jobs = Job.query.all()
    applications = Application.query.all()
    return render_template('admin.html', users=users, jobs=jobs, applications=applications)


# ── Admin Delete User ──────────────────────────────────────────
@app.route('/admin/delete-user/<int:user_id>')
@login_required
def delete_user(user_id):
    if current_user.role != 'admin':
        return redirect(url_for('index'))
    user = User.query.get_or_404(user_id)
    db.session.delete(user)
    db.session.commit()
    flash('User deleted!', 'success')
    return redirect(url_for('admin_panel'))


if __name__ == '__main__':
    app.run(debug=True)
