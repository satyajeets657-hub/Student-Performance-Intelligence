# Student Performance Intelligence System

![Python](https://img.shields.io/badge/Python-3.10%2B-blue?logo=python)
![Flask](https://img.shields.io/badge/Framework-Flask%203.1-black?logo=flask)
![Database](https://img.shields.io/badge/Database-SQLite3-blue?logo=sqlite)
![Status](https://img.shields.io/badge/Status-Production%20Ready-brightgreen)
![License](https://img.shields.io/badge/License-Academic-orange)

> **Presented by:** Satyajeet Singh  
> **Department:** Department of Data Science  
> **Documentation:** [PROJECT_REPORT.md](PROJECT_REPORT.md) | [WORK_LOG.md](WORK_LOG.md) | [Printable Report (HTML)](PROJECT_REPORT_PRINTABLE.html)

---

## 📌 Executive Overview
The **Student Performance Intelligence System** is an explainable, transparent academic analytics and decision-support web platform. Unlike opaque "black-box" machine learning algorithms, this platform employs a **deterministic, rule-based mathematical model** to evaluate student performance across academics, continuous assessments, attendance, and study habits.

### ✨ Innovative Features
- **Composite Performance Score (0 - 100):** Balanced multi-criteria formulation weighting exams, labs, assignments, quizzes, and study hours.
- **5-Tier Performance Status:** Categorizes students into *Excellent*, *Good*, *Stable*, *Attention*, and *High Risk*.
- **Early Warning Support Flag:** Automatically detects at-risk students before final examinations based on multi-factor thresholds.
- **Department Benchmark & Performance Gap:** Compares individual achievement against departmental averages ($\text{Score} - \text{Dept. Avg}$).
- **Actionable Pedagogical Insights:** Generates clear, non-generic recommendations (e.g., *"Improve attendance"*, *"Focus on quizzes"*).
- **Interactive "What-If" Scenario Simulator:** Allows students to adjust sliders for attendance and study hours to simulate projected score improvements in real time.
- **Supervised Machine Learning Models (scikit-learn):** Dual Random Forest Regressor and Classifier predicting final examination marks ($R^2=0.62, \text{MAE}=4.29$) and identifying at-risk support tiers with **91.0% accuracy** alongside Explainable AI feature importances.
- **Generative AI Study Mentor & Pedagogical Advisor:** Powered by **Google Gemini 1.5 Flash** with zero-downtime offline fallback, drafting customized 7-day study timetables, parent advisory letters, and 4-week faculty remedial roadmaps.
- **Dedicated Portals:** Separate, secure interfaces for Teachers and Students with Role-Based Access Control (RBAC).
- **Local AI Query Assistant:** Natural language query engine answering educator questions without requiring external API tokens.

---

## 🚀 Live Demo & Deployment

### Option 1: 1-Click Free Cloud Deployment (Render.com)
This repository includes ready-to-use [`render.yaml`](render.yaml) and [`Procfile`](Procfile) for free hosting:
1. Fork or push this repository to your GitHub account.
2. Sign in to [Render.com](https://render.com) with GitHub.
3. Click **New +** &rarr; **Web Service** &rarr; Select your repository.
4. Render automatically configures:
   - **Environment:** Python
   - **Build Command:** `pip install -r requirements.txt`
   - **Start Command:** `gunicorn wsgi:app`
5. Click **Create Web Service**. Your live link (`https://<your-app>.onrender.com`) will be active in minutes with free SSL!

### Option 2: Running Locally
```bash
# 1. Clone repository
git clone https://github.com/<your-username>/student-performance-intelligence.git
cd student-performance-intelligence

# 2. Install dependencies
pip install -r requirements.txt

# 3. Launch application
python wsgi.py
```
Open **`http://127.0.0.1:5000`** in your browser.

---

## 🔑 Demo Login Credentials
| Role | Username | Password | Purpose |
|---|---|---|---|
| **Teacher / Admin** | `teacher` | `teacher123` | Class cockpit, AI assistant, risk flags, student drill-downs |
| **Student (Demo 1)** | `ST0001` | `student123` | Personal scorecard, What-If simulator, recommendations |
| **Student (Demo 2)** | `ST0002` | `student123` | Alternate student profile with different academic metrics |

---

## 🖨️ How to Print Your Project Report
For exams, submissions, presentations, or studying offline:
1. Open [`PROJECT_REPORT_PRINTABLE.html`](PROJECT_REPORT_PRINTABLE.html) in Chrome or Edge.
2. Click **Print / Save as PDF** (or press `Ctrl + P`).
3. Select **"Save as PDF"** or choose your physical printer.
4. The document includes clean A4 formatting, page breaks, formulas, and viva questions ready for study!

---

## 📂 Repository Structure
```
├── PROJECT_REPORT.md            # Comprehensive Master Academic Report
├── PROJECT_REPORT_PRINTABLE.html# Print-Ready HTML report (Ctrl+P to print)
├── WORK_LOG.md                  # Detailed chronological work & changelog
├── README.md                    # Project landing page
├── requirements.txt             # Python dependencies
├── wsgi.py                      # WSGI production server entrypoint
├── render.yaml                  # Render cloud deployment blueprint
├── Procfile                     # Web process declaration for cloud
├── .gitignore                   # Ignored files (caches, logs, virtual environments)
├── data/
│   └── students.csv             # 500 synthetic student benchmark records
├── notebooks/
│   └── student_analysis.py      # Standalone data analytics and CSV exporter
├── outputs/
│   ├── student_performance_analysis_final.csv
│   └── students_needing_support.csv
├── presentation/
│   └── Student_Performance_Analysis_Final_Aesthetic_Professional.pptx
├── reports/
│   └── Student_Performance_Analysis_System.docx
├── uploads/
│   └── learning_materials/      # Course notes and reference documents
└── web/
    ├── app.py                   # Flask backend and AI assistant logic
    ├── student_intelligence.db  # SQLite database instance
    ├── static/style.css         # Responsive styling
    └── templates/               # HTML5 templates (teacher, student, login, index)
```

---

## 📊 Performance Score Formulation
The composite performance score is computed using the following weights:

$$\text{Study Score} = \min\left(\frac{\text{Study Hours}}{6} \times 100, 100\right)$$

$$\text{Performance Score} = (0.35 \times \text{Final Marks}) + (0.15 \times \text{Attendance}) + (0.10 \times \text{Study Score}) + (0.10 \times \text{Assignment Score}) + (0.10 \times \text{Quiz Average}) + (0.10 \times \text{Practical Score}) + (0.10 \times \text{Internal Marks})$$

---

## 👨‍💻 Author
**Satyajeet Singh**  
*Department of Data Science*  
Student Performance Intelligence System
