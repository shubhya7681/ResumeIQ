# ResumeIQ – AI Resume Analyzer & Career Guidance Portal

ResumeIQ is a premium, full-stack AI-powered web application that analyzes resumes, calculates ATS compatibility, detects skills, recommends job roles, and generates personalized career roadmaps and interview questions.

## Features

- **Authentication System:** Secure signup/login with session management and separate User/Admin roles.
- **Resume Upload:** Drag-and-drop support for PDF and DOCX files.
- **AI Analysis:** 
  - Resume Scoring (0-100)
  - ATS Compatibility Score
  - Strengths & Weaknesses Detection
  - Missing Sections Identification
- **Skill Detection:** NLP-based detection of 150+ technical and soft skills across multiple categories.
- **Job Role Prediction:** Recommends optimal job roles based on detected skill profiles.
- **Interview Question Generator:** Automatically generates skill-based interview questions with varying difficulty levels.
- **Career Roadmap:** Structured learning paths for different career roles.
- **Admin Dashboard:** Comprehensive view of users, uploaded resumes, and platform analytics.
- **Beautiful UI:** Premium dark-themed, glassmorphism UI with responsive design and smooth animations.

## Tech Stack

- **Frontend:** HTML5, CSS3 (Custom Vanilla/Glassmorphism), JavaScript, Chart.js, FontAwesome
- **Backend:** Python, Flask
- **Database:** SQLite with SQLAlchemy ORM
- **AI/NLP:** custom Python NLP pre-processing, regex-based skill/pattern matching
- **File Parsing:** pdfplumber, python-docx
- **PDF Generation:** ReportLab

## Project Structure

```text
Resume Project/
├── app.py                      # Main Flask application
├── config.py                   # Configuration settings
├── requirements.txt            # Python dependencies
├── README.md                   # Project documentation
├── database/                   # SQLite database directory
│   └── resumeiq.db             # Auto-generated database file
├── models/
│   ├── __init__.py
│   └── models.py               # SQLAlchemy database models
├── utils/
│   ├── __init__.py
│   ├── analyzer.py             # Resume scoring and analysis
│   ├── career_roadmap.py       # Career paths data
│   ├── interview_questions.py  # Interview question generation
│   ├── job_predictor.py        # Role prediction logic
│   ├── report_generator.py     # PDF report generation
│   ├── resume_parser.py        # PDF/DOCX text extraction
│   └── skill_detector.py       # NLP skill detection engine
├── static/
│   ├── css/
│   │   └── style.css           # Premium styling
│   └── js/
│       └── main.js             # Interactive UI logic
├── templates/                  # HTML templates
│   ├── admin.html
│   ├── analysis.html
│   ├── base.html
│   ├── career_roadmap.html
│   ├── contact.html
│   ├── dashboard.html
│   ├── index.html
│   ├── login.html
│   ├── signup.html
│   └── upload.html
└── uploads/                    # User uploaded resumes (auto-created)
```

## Setup Instructions

1. **Install Python 3.8+**

2. **Create a virtual environment (optional but recommended):**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows use: venv\Scripts\activate
   ```

3. **Install Dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

4. **Run the Application:**
   ```bash
   python app.py
   ```
   The application will automatically create the SQLite database and default admin user upon first run.

5. **Access the App:**
   Open your browser and navigate to `http://127.0.0.1:5000`

## Demo Accounts

- **Admin Account:**
  - Email: `admin@resumeiq.com`
  - Password: `admin123`

- **User Account:** Create your own via the Sign Up page.

## generating Sample Resumes
To generate sample resumes for testing, you can use the `generate_samples.py` script provided in the project folder (if created), or just upload any PDF/DOCX file.
