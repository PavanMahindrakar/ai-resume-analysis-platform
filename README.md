# 🚀 AI Resume Analysis Platform

### Explainable Resume–Job Description Matching System

<div>

**A full-stack web application that analyzes resumes against job descriptions using transparent, explainable NLP techniques**

![Python](https://img.shields.io/badge/Python-3.11+-blue.svg)
![FastAPI](https://img.shields.io/badge/FastAPI-0.109-green.svg)
![React](https://img.shields.io/badge/React-18-blue.svg)
![TypeScript](https://img.shields.io/badge/TypeScript-5.2-blue.svg)
![PostgreSQL](https://img.shields.io/badge/PostgreSQL-14+-blue.svg)

</div>

---

## Table of Contents
- [Overview](#-overview)
- [Features](#-key-features)
- [Tech Stack](#-technology-stack)
- [Architecture](#-system-architecture)
- [API](#-api-overview)
- [Quick Start](#-quick-start)
- [Contributing](#-contributing)

---

## 🎯 Overview

**AI Resume Analysis Platform** is a Python full-stack application that helps job seekers understand how well their resume matches a job description — and *why*.

Most Applicant Tracking Systems (ATS) behave like black boxes, offering little feedback to candidates. This project focuses on **explainability**, clearly showing which skills matched, which were missing, and how the final score was calculated.

### Why this matters

* Job seekers receive actionable feedback instead of silent rejections
* Matching logic is transparent and technically defensible
* No black-box models — every decision can be traced

---

## ✨ Key Features

### 🔐 Authentication

* JWT-based authentication
* Secure password hashing using bcrypt
* User-level data isolation

### 📄 Resume Processing

* PDF resume upload
* Automatic text extraction
* Resume history management

### 💼 Job Description Analysis

* Job description storage
* Keyword and skill extraction
* Historical tracking

### 🔍 Explainable Matching Engine

* Resume ↔ job description comparison
* Match score (0–100%)
* Missing skill detection
* Human-readable explanations
* Importance-weighted scoring using TF-IDF

### 📊 Interactive Dashboard

* Analysis history
* Match score trends
* Common missing skills
* Clickable analysis details

### 🎨 Frontend Experience

* Drag-and-drop uploads
* Loading and error states
* Responsive design
* Dark / light mode
* Accessible UI

---

## 🛠 Technology Stack

### Backend

* Python 3.11
* FastAPI
* SQLAlchemy
* PostgreSQL
* Alembic
* JWT (python-jose)
* bcrypt
* scikit-learn (TF-IDF)
* PDFMiner
* Pytest

### Frontend

* React 18
* TypeScript
* React Router
* Axios
* Context API
* Recharts
* React Dropzone
* Vite

### AI / NLP

* TF-IDF keyword extraction
* Rule-based keyword matching
* Fully explainable logic (no neural networks)

---

## 🏗 System Architecture

```
React (TypeScript)
      ↓
FastAPI (Python)
      ↓
Matching Engine (TF-IDF + Rules)
      ↓
PostgreSQL
```

### Data Flow

1. Resume uploaded → PDF parsed → text extracted
2. Job description created → keywords extracted
3. Matching engine compares both
4. Score and explanations generated
5. Results stored and visualized

---

## 🔬 Explainable Matching Logic (Core Innovation)

### Why TF-IDF?

* Well-established information retrieval technique
* Importance-weighted keywords
* Fully transparent scoring
* Easy to explain in interviews

### Match Score Formula

```
Match Score = (Matched Keywords / Total Job Keywords) × 100
```

Weighted by:

* Keyword importance (TF-IDF score)
* Exact vs partial matches

### Output Includes

* Final match score
* Matched skills
* Missing skills (ranked)
* Plain-English explanation

This approach prioritizes **clarity and trust** over opaque accuracy.

---

## 📡 API Overview

### Authentication

```
POST /api/v1/auth/register
POST /api/v1/auth/login
```

### Resume

```
POST /api/v1/resume/upload
GET  /api/v1/resumes
```

### Job Description

```
POST /api/v1/job-description/create
GET  /api/v1/job-descriptions
```

### Analysis

```
POST /api/v1/analysis/run
GET  /api/v1/analysis/{id}
```

### Dashboard

```
GET /api/v1/dashboard/summary
GET /api/v1/dashboard/history
```

---

## 🚀 Quick Start

### Backend

```bash
cd backend
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
cp .env.example .env
alembic upgrade head
uvicorn app.main:app --reload
```

### Frontend

```bash
cd frontend
npm install
cp .env.example .env
npm run dev
```

---

## 🧪 Testing

* Unit tests for matching logic and security
* Integration tests for APIs
* Pytest with coverage support

```bash
pytest --cov=app
```

---

## 🚀 Future Enhancements

* Semantic similarity using word embeddings
* Skill synonym dictionary
* Resume version comparison
* Job application tracking
* Background processing (Celery)
* Caching with Redis

---

## 🤝 Contributing

Contributions, issues, and feature requests are welcome.

If you would like to contribute:

1. Fork the repository
2. Create a new branch (`feature/your-feature-name`)
3. Commit your changes with clear messages
4. Open a Pull Request describing your changes

Please ensure code is well-documented and follows existing project structure.

---

## 👤 Author

**Pavan Mahindrakar**
Aspiring Software Engineer | Python & Full-Stack Developer

* GitHub:  [@PavanMahindrakar](https://github.com/PavanMahindrakar)


---

## 📄 License

This project is licensed under the **MIT License**.

---

<div align="center">

**Built with ❤️ using FastAPI, React, and PostgreSQL**

[Back to Top](#-ai-resume-analysis-platform)

</div>
