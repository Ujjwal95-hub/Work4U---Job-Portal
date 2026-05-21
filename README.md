# 💼 Work4U — Job Portal Web Application

> A full-stack job portal built with Python Flask, SQLite, and Bootstrap 5.
> Developed as a Final Project for Python Developer Internship.
---

## 🌟 Features

### 👤 Three User Roles
| Role | Capabilities |
|---|---|
| **Job Seeker** | Register, browse jobs, search with filters, apply with one click, track applications |
| **Employer** | Register, post jobs, manage listings, view applicants |
| **Admin** | Manage all users, jobs, and applications from a central dashboard |

### ⚡ Core Features
- 🔐 Secure user authentication (Register/Login/Logout)
- 📋 Job posting with title, description, salary, location & category
- 🔍 Job search with filters (keyword, location, category)
- 📝 One-click job application system
- 📊 Dashboard for each role
- 🛡️ Admin panel to manage entire platform
- 🎨 Smooth page animations & transitions
- 📱 Fully responsive design

---

## 🛠️ Tech Stack

| Layer | Technology |
|---|---|
| **Backend** | Python, Flask, Flask-SQLAlchemy, Flask-Login |
| **Frontend** | HTML5, CSS3, Bootstrap 5, JavaScript |
| **Database** | SQLite |
| **Security** | Werkzeug Password Hashing |
| **Deployment** | Gunicorn, Render |

---

## 📁 Project Structure

```
Work4U/
├── main.py                    # Main Flask app & all routes
├── models.py                  # Database models (User, Job, Application)
├── requirements.txt           # Project dependencies
├── README.md                  # Project documentation
├── work4u.db                  # SQLite database
├── templates/
│   ├── base.html              # Base layout with navbar & footer
│   ├── index.html             # Home page
│   ├── login.html             # Login page
│   ├── register.html          # Registration page
│   ├── jobs.html              # Job listings with search
│   ├── job_detail.html        # Job detail & apply
│   ├── post_job.html          # Employer job posting form
│   ├── seeker_dashboard.html  # Job seeker dashboard
│   ├── employer_dashboard.html# Employer dashboard
│   └── admin.html             # Admin panel
└── static/
    ├── style.css              # Custom styles & animations
    └── script.js              # Animations & interactivity
```

---

## ⚙️ Setup & Installation

### Prerequisites
- Python 3.x installed
- pip package manager

### Step 1 — Clone the Repository
```bash
git clone git clone https://github.com/Ujjwal95-hub/Work4U---Job-Portal.git
cd Work4U
```

### Step 2 — Install Dependencies
```bash
pip install -r requirements.txt
```

### Step 3 — Run the Application
```bash
python main.py
```

### Step 4 — Open in Browser
```
http://127.0.0.1:5000
```

---

## 🔑 Default Credentials

| Role | Email | Password |
|---|---|---|
| Admin | admin@work4u.com | admin123 |
| Employer | Register yourself | Your choice |
| Job Seeker | Register yourself | Your choice |

---

## 📸 Screenshots

### 🏠 Home Page
- Hero section with job search
- Latest job listings
- Browse by category

### 📋 Job Listings
- Search by keyword, location, category
- Clean job cards with salary & location

### 🛡️ Admin Panel
- Manage all users & jobs
- View all applications

---

## 🚀 Deployment

This project is deployed on **Render**:
- 🔗 Live URL: `https://work4u.onrender.com` *(update after deployment)*

### Deploy on Render:
1. Push code to GitHub
2. Go to [render.com](https://render.com)
3. New Web Service → Connect GitHub repo
4. Set **Start Command**: `gunicorn main:app`
5. Deploy! 🎉

---

## 👨‍💻 Developer

**Ujjwal Gupta - Python Developer Intern**
- 💻 Python Developer
- 🐙 GitHub: [Ujjwal95-hub](https://github.com/Ujjwal95-hub)
- 💼 LinkedIn: [ujjwal-gupta95](https://www.linkedin.com/in/ujjwal-gupta95)

---

## 📄 License

© 2026 Work4U — Ujjwal Gupta. All Rights Reserved.