# ResumeIQ: An AI-Powered Resume Analysis and Career Guidance Platform

**[Project Report / Research Paper]**

> **Authors:** [Your Name(s)] · [Your Department] · [Your Institution]  
> **Submitted:** May 2026  
> **Keywords:** Applicant Tracking System (ATS), Resume Parsing, Natural Language Processing, Career Guidance, Flask, Skill Detection

---

## Abstract

In the modern job market, candidates frequently struggle to align their resumes with Applicant Tracking System (ATS) requirements, leading to premature rejection. This paper presents **ResumeIQ**, an intelligent, full-stack web application designed to evaluate resumes, extract key professional skills, predict suitable job roles, and provide personalized career roadmaps. Leveraging Python-based NLP techniques, rule-based pattern matching, and an interactive Flask frontend, ResumeIQ provides candidates with a comprehensive 0-100 ATS compatibility score, detects over 150 categorized technical and soft skills, and automatically generates tailored interview questions. By addressing the gap between candidate presentation and automated recruiter screening, ResumeIQ serves as an accessible, high-performance career optimization tool.

---

## 1. Introduction

Recruitment processes have become increasingly automated, with up to 75% of resumes being discarded by Applicant Tracking Systems (ATS) before human review. Candidates often lack feedback on why their resumes were rejected, whether due to missing keywords, poor formatting, or a lack of quantifiable achievements. 

While enterprise solutions exist for recruiters, tools designed specifically for candidates are often expensive, locked behind paywalls, or lack transparent feedback mechanisms. **ResumeIQ** was developed to democratize this technology, providing an open, transparent, and highly interactive platform for job seekers to optimize their profiles.

### 1.1 Objectives

1. **Automated Resume Parsing:** Extract text reliably from both PDF and DOCX formats.
2. **Skill Taxonomy & Detection:** Identify exact skill matches using a robust, multi-category taxonomy and NLP heuristics.
3. **Role Prediction:** Map detected skill sets to the most statistically probable job titles.
4. **Actionable Feedback:** Provide an overall ATS score, highlight missing foundational skills, and identify missing resume sections.
5. **Interactive Guidance:** Generate role-specific interview questions and structured learning roadmaps.

---

## 2. System Architecture

ResumeIQ is built using a decoupled but cohesive **Model-View-Controller (MVC)** architecture.

```text
┌─────────────────────────────────────────────────────────┐
│                     Client (Browser)                    │
│    Drag & Drop Upload → Dynamic UI → Data Visualization │
└────────────────────────┬────────────────────────────────┘
                         │ Multi-part Form (PDF/DOCX)
                         ▼
┌─────────────────────────────────────────────────────────┐
│                 Flask Backend (app.py)                  │
│  ┌──────────────┐  ┌───────────────┐  ┌─────────────┐  │
│  │ User Auth    │  │ Admin Routing │  │ PDF/Docx I/O│  │
│  └──────┬───────┘  └──────┬────────┘  └──────┬──────┘  │
└─────────│─────────────────│──────────────────│──────────┘
          │                 │                  │
          ▼                 ▼                  ▼
┌─────────────────────────────────────────────────────────┐
│                  Analysis Engine (utils/)               │
│  - resume_parser.py (Text extraction & normalization)   │
│  - skill_detector.py (Regex NLP pattern matching)       │
│  - job_predictor.py (Rule-based role classification)    │
│  - analyzer.py (ATS Scoring & Section heuristics)       │
│  - interview_questions.py & career_roadmap.py           │
└────────────────────────┬────────────────────────────────┘
                         │
                         ▼
┌─────────────────────────────────────────────────────────┐
│               Data Persistence (SQLite)                 │
│        User Profiles · Upload History · Analysis        │
└─────────────────────────────────────────────────────────┘
```

---

## 3. Methodology

### 3.1 Text Extraction and Normalization (`resume_parser.py`)
The system accepts `.pdf` and `.docx` file formats. PDFs are processed using the `pdfplumber` library to extract layout-aware text, while `.docx` files are parsed via `python-docx`. The raw text undergoes normalization, which involves:
- Lowercasing and whitespace stripping.
- Removing non-alphanumeric noise characters.
- Handling special characters commonly found in IT skill names (e.g., C++, .NET, Node.js).

### 3.2 Skill Detection Engine (`skill_detector.py`)
Instead of relying on heavy machine learning models that require immense computational overhead, ResumeIQ employs a **Lexicon-Based Regex Engine** optimized for speed and accuracy.

- **Taxonomy:** The system utilizes a curated dictionary (`SKILL_DATABASE`) containing over 150 skills categorized into 8 domains: *Programming Languages, Web Technologies, Frameworks, Data Science & ML, Databases, Cloud & DevOps, Tools & Platforms, and Soft Skills*.
- **Pattern Matching:** To prevent false positives (e.g., detecting the letter "C" as the programming language in the word "Cat"), the engine uses sophisticated regex word boundaries (`\b`) and lookaround assertions.
- **Suggestion Algorithm:** Based on the identified skills, a ruleset suggests complementary skills (e.g., if `Python` is found, `Flask` or `Pandas` are suggested).

### 3.3 Scoring and ATS Analysis (`analyzer.py`)
The resume score (0-100) is calculated via a weighted multi-factor heuristic model:
1. **Word Count (15%):** Penalizes abnormally short (<150 words) or exceedingly long (>1000 words) resumes.
2. **Skill Density (40%):** Rewards resumes that mention a diverse range of categorized skills, capped at a reasonable threshold to prevent keyword stuffing.
3. **Section Detection (30%):** Scans for critical sections (Education, Experience, Projects, Skills) using synonym matching (e.g., "Work History", "Professional Experience").
4. **Action Verb Usage (15%):** Evaluates the presence of strong action verbs (e.g., *developed, managed, orchestrated*) indicating quantifiable achievements.

### 3.4 Job Role Prediction (`job_predictor.py`)
The system maps the detected skill array against predefined role vectors (e.g., Frontend Developer, Data Scientist, Cloud Engineer). It calculates a match percentage for each role based on the overlap of critical required skills and returns the top 3 highest-matching professions.

### 3.5 Career Guidance Generation
- **Interview Questions (`interview_questions.py`):** Based on the top detected skills, the system retrieves relevant technical questions to assist in interview preparation.
- **Career Roadmap (`career_roadmap.py`):** Provides a step-by-step learning progression tailored to the user's predicted or desired job role, outlining beginner, intermediate, and advanced milestones.

---

## 4. Implementation Details

### 4.1 Technology Stack
| Layer | Technology | Purpose |
|---|---|---|
| **Frontend** | HTML5, CSS3, JavaScript | UI structure, custom Glassmorphism styling |
| **Data Viz** | Chart.js | Visualizing skill distribution and ATS scores |
| **Backend** | Python (Flask) | Server logic, routing, file handling |
| **Database** | SQLite + SQLAlchemy | Secure relational data storage and ORM |
| **Parsing** | pdfplumber, python-docx | High-fidelity document text extraction |
| **Security** | Werkzeug Security | Password hashing and session management |

### 4.2 User Flow
1. **Authentication:** Users register and log in to a secure session.
2. **Upload:** A drag-and-drop interface accepts the resume file.
3. **Processing:** The Flask backend routes the file to the `utils/` pipeline, which generates an analysis dictionary.
4. **Visualization:** The server renders `analysis.html`, presenting the scores, skill badges, and charts dynamically using Jinja2 templating.

### 4.3 Admin Dashboard
A dedicated admin role provides a macroscopic view of platform usage, allowing administrators to view total registered users, track upload volume, and preview database statistics to monitor the platform's health.

---

## 5. Limitations & Future Scope

While highly effective, the current rule-based architecture presents specific limitations:
1. **Contextual Blindness:** The regex engine identifies the presence of a skill but cannot verify the *depth* of experience. (e.g., "I read about Python" triggers the same match as "Developed backend in Python").
2. **Hardcoded Taxonomies:** New technologies must be manually added to `SKILL_DATABASE`.

**Future Enhancements:**
- Integration with LLM APIs (like Google Gemini or OpenAI) to perform semantic understanding of the candidate's experience bullet points.
- Integration with live Job Board APIs to fetch real-time matching job postings.
- Dynamic PDF Resume generation based on the optimized data.

---

## 6. Conclusion

**ResumeIQ** successfully bridges the gap between candidates and automated tracking systems by providing a lightweight, transparent, and highly educational platform. By utilizing optimized NLP parsing and a responsive, modern UI, the application delivers immediate value to job seekers, helping them identify weaknesses, upskill through roadmaps, and ultimately increase their chances of passing recruiter screenings.

---

## References

1. Bogen, M., & Rieke, A. (2018). *Help Wanted: An Examination of Hiring Algorithms, Equity, and Bias*. Upturn.
2. Nacer, H., & Aissani, A. (2014). *Semantic Information Retrieval from Resumes using NLP*. International Journal of Computer Applications.
3. *Flask Documentation (v3.0)*. Pallets Projects. https://flask.palletsprojects.com/
4. *Chart.js Documentation*. https://www.chartjs.org/docs/latest/
5. *pdfplumber GitHub Repository*. https://github.com/jsvine/pdfplumber

---
*End of Report*
