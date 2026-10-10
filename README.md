# LokLens — A Lens Through Development

> **Civic Technology / Government Accountability Platform**  
> Tracking election manifesto promises and examining on-ground implementation records using documented official sources.

[![Python](https://img.shields.io/badge/Python-3.13-blue.svg)](https://www.python.org/)
[![Flask](https://img.shields.io/badge/Flask-3.1-black.svg)](https://flask.palletsprojects.com/)
[![MySQL](https://img.shields.io/badge/MySQL-9.7-orange.svg)](https://www.mysql.com/)
[![License](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)
[![Tests](https://img.shields.io/badge/Tests-66%20Passed-brightgreen.svg)]()

---

## 1. Project Overview & Problem Statement

### The Problem
During election cycles, political parties publish extensive manifestos containing promises to citizens. However, ordinary voters and civil society organizations struggle to verify what happens after elections:
- There is no central, evidence-based portal tracking on-ground implementation.
- Media coverage is fragmented and often lacks primary source documentation.
- Existing trackers often misclassify recurring welfare entitlements (e.g. cash transfers or electricity subsidies) into misleading "percentage completion" bars designed for infrastructure projects.

### The Solution: LokLens
**LokLens** is an open, citizen-first civic accountability web platform. It enables citizens to:
1. Explore election promises made by state administrations.
2. Examine verified on-ground implementation metrics (e.g., consumer accounts covered, zero-fare bus trips, DBT disbursement rounds).
3. Access primary source documents — including the original party manifesto PDF and official departmental Government Orders (G.O.).
4. Transparently review policy adjustments (such as grain-to-cash conversions) without obscured data.

*Initial Focus:* Karnataka and the **5 Flagship Guarantees** from the Karnataka Congress 2023 Assembly Election Manifesto.

---

## 2. Key Features

- **Evidence-Driven Tracking**: Every promise cites its implementing department, Government Order (G.O.) number, and source publication.
- **Scheme-Appropriate Metrics**: Measures schemes by their authentic units (kWh energy waivers, passenger trips, DBT cash amounts) rather than fabricated completion percentages.
- **Interactive Multi-State Architecture**: Seamless state switching with clear, honest empty states for regions whose records are undergoing verification.
- **Real-Time Client Filtering**: Instant search across scheme names, benefit amounts, and keywords, paired with category filter pills (Energy, Women Welfare, Food Security, Youth & Jobs, Transport).
- **Accessible Detail Modal**: Fully keyboard-accessible (`Escape` key dismissal, focus trapping, screen-reader ARIA landmarks) detail view.
- **Full-Stack REST Architecture**: Powered by Python Flask and MySQL, with graceful offline fallback to local verified datasets when running without server infrastructure.
- **Automated Test Coverage**: 66 unit and integration test assertions verifying backend REST routes, database queries, and frontend DOM integrity.

---

## 3. Technology Stack

### Frontend
- **HTML5**: Semantic document landmarks (`<header>`, `<main>`, `<article>`, `<dialog>`/modal).
- **CSS3**: Custom design system using CSS Variables (`:root`), Flexbox, CSS Grid, and subtle glassmorphism (`backdrop-filter`).
- **JavaScript (ES6+)**: Vanilla JavaScript utilizing `async/await`, the `fetch()` API, Event Delegation, and reactive state management (`appState`).

### Backend
- **Python 3.13**: Core programming language.
- **Flask 3.1**: Lightweight, performant microframework for REST APIs and static file delivery.
- **Flask-CORS**: Enables Cross-Origin Resource Sharing.
- **python-dotenv**: 12-Factor App environment variable configuration.
- **PyMySQL**: Native MySQL database driver with parameterized queries.

### Database
- **MySQL 9.7**: Relational Database Management System (RDBMS) configured in Third Normal Form (3NF).

---

## 4. Architecture & System Flow

```
┌─────────────────────────────────────────────────────────────┐
│                       CLIENT BROWSER                        │
│                                                             │
│   [ State Picker ]     [ Search Input ]    [ Category Pills]│
│                           │                                 │
│                           ▼                                 │
│                   script.js (appState)                      │
│                           │                                 │
│                HTTP Fetch /api/promises                     │
└───────────────────────────┼─────────────────────────────────┘
                            │ REST JSON API
┌───────────────────────────┼─────────────────────────────────┐
│                           ▼                                 │
│                   FLASK BACKEND (app.py)                    │
│                           │                                 │
│                   db.py (Repository)                        │
│                           │                                 │
│                  PyMySQL / Connection Pool                  │
└───────────────────────────┼─────────────────────────────────┘
                            │ SQL Queries
┌───────────────────────────▼─────────────────────────────────┐
│                      MYSQL (loklens_db)                     │
│                                                             │
│   states  ───< administrations ───< manifestos ───< promises│
│                                                        │    │
│                                                 promise_sources
│                                                        │    │
│                                                     sources │
└─────────────────────────────────────────────────────────────┘
```

---

## 5. Project Folder Structure

```text
manifesto Project/
├── .env.example                                               # Template for environment secrets
├── .gitignore                                                 # Protects credentials & bytecode
├── Assembly_Election_Karnataka_Manifesto_2023_241fdc08d0.pdf  # Primary source manifesto document
├── app.py                                                     # Flask REST API & static file host
├── data.js                                                    # Offline verified dataset store
├── db.py                                                      # MySQL connection & repository layer
├── index.html                                                 # Dashboard frontend template
├── init_db.py                                                 # Automated database setup script
├── requirements.txt                                           # Python dependencies
├── schema.sql                                                 # Relational schema DDL & seed data
├── script.js                                                  # Interactive frontend controller
├── style.css                                                  # Deep navy civic-tech design system
├── test_api.py                                                # Backend automated test suite (12 tests)
├── test_frontend.js                                           # Frontend DOM & data test suite (54 tests)
└── wsgi.py                                                    # Production WSGI server entry point
```

---

## 6. Database Schema Design

The relational database (`loklens_db`) consists of 6 tables normalized to Third Normal Form (3NF):

1. **`states`**: `(id [PK], name, has_data, unverified_message, created_at)`
2. **`administrations`**: `(id [PK], state_id [FK], party_name, term_years, created_at)`
3. **`manifestos`**: `(id [PK], administration_id [FK], title, subtitle, document_path, published_year)`
4. **`promises`**: `(id [PK], manifesto_id [FK], state_id [FK], name, category, status, summary, manifesto_quote, implementation_details, target_metric, delivered_metric, metric_type, reporting_period, data_notes)`
5. **`sources`**: `(id [PK], title, url, source_type, created_at)`
6. **`promise_sources`**: Many-to-Many junction table linking `(promise_id [FK], source_id [FK])`.

---

## 7. REST API Reference

All endpoints return JSON responses with standard HTTP status codes (`200 OK`, `400 Bad Request`, `404 Not Found`).

### Core Endpoints

#### 1. System Health Check
- **`GET /api/health`**
- *Response:*
  ```json
  {
    "status": "healthy",
    "application": "LokLens — A Lens Through Development",
    "database": "mysql_connected",
    "version": "1.0.0"
  }
  ```

#### 2. List Supported States
- **`GET /api/states`**
- *Response:* Returns array of all 5 states, indicating `hasData: true/false`.

#### 3. List Manifesto Promises (with Filters)
- **`GET /api/promises?state=karnataka&category=energy&search=200`**
- *Query Parameters:*
  - `state` (optional, default: `karnataka`)
  - `category` (optional, e.g., `energy`, `women`, `food`, `youth`, `transport`)
  - `search` (optional keyword search)
- *Response:*
  ```json
  {
    "state": "Karnataka",
    "hasData": true,
    "count": 1,
    "totalGuarantees": 5,
    "promises": [ ... ]
  }
  ```

#### 4. Get Detailed Promise by ID
- **`GET /api/promises/<promise_id>`** (e.g. `/api/promises/gruha-jyothi`)
- *Response:* Complete scheme profile with Department, G.O. number, eligibility, metrics, and sources.

#### 5. Get Promise Progress & Metric Record
- **`GET /api/promises/<promise_id>/progress`**
- *Response:* Specific progress metrics, reporting periods, and transparency notes.

#### 6. List Consolidated Official Sources
- **`GET /api/sources`**
- *Response:* Array of all documented gazettes, Government Orders, and manifesto documents.

---

## 8. Installation & Setup Guide

### Prerequisites
- Python 3.10+ (Tested on Python 3.13)
- MySQL Server 8.0+ or 9.0+
- Node.js (Optional, for running frontend test script)

### Step 1: Clone or Navigate to the Project
```powershell
cd "C:\Users\ANSAR\OneDrive\Desktop\manifesto Project"
```

### Step 2: Install Python Dependencies
```powershell
python -m pip install -r requirements.txt
```

### Step 3: Configure Database Environment Variables
1. Copy `.env.example` to `.env`:
   ```powershell
   Copy-Item .env.example .env
   ```
2. Open `.env` in an editor and enter your local MySQL password:
   ```ini
   DB_HOST=localhost
   DB_PORT=3306
   DB_USER=root
   DB_PASSWORD=your_actual_mysql_password
   DB_NAME=loklens_db
   ```

### Step 4: Initialize and Seed the Database
Run the one-click setup script:
```powershell
python init_db.py
```
*(Creates `loklens_db`, builds all 6 tables, and seeds the 5 Karnataka 2023 guarantees).*

### Step 5: Start the Application Server
```powershell
python app.py
```
Navigate to **`http://127.0.0.1:5000`** in your browser.

---

## 9. Running Automated Tests

LokLens includes automated test suites covering both the backend and frontend.

### Run Backend Unit & Integration Tests (12 Tests)
```powershell
python test_api.py
```
*Expected Output:*
```text
............
----------------------------------------------------------------------
Ran 12 tests in 3.328s

OK
```

### Run Frontend & Civic Data Integrity Tests (54 Tests)
```powershell
node test_frontend.js
```
*Expected Output:*
```text
Results: 54 Passed, 0 Failed.
```

---

## 10. Karnataka 2023 5 Guarantees — Vetted Data

| Guarantee | Department & G.O. Reference | Promised Benefit | Appropriate Metric Unit | Real-World Status |
| :--- | :--- | :--- | :--- | :--- |
| **Gruha Jyothi** | Energy Dept (G.O. EN 22 PSR 2023) | Up to 200 units free power/month | Power consumption (kWh) & zero-bill domestic accounts | **Delivered / Active** |
| **Gruha Lakshmi** | Women & Child Dev (G.O. WCD 90 MMB 2023) | ₹2,000/month to woman head of family | Monthly Direct Benefit Transfer (DBT) | **Delivered / Active** |
| **Anna Bhagya** | Food & Civil Supplies (G.O. FCS 47 RPR 2023) | 10 kg food grains per BPL individual | Grain distribution (kg) + Cash transfer (₹) | **Partly Cash / Active** (5 kg rice + ₹170 cash via DBT) |
| **Yuvanidhi** | Skill Development (G.O. SDEL 57 TPE 2023) | ₹3,000 (Grads) / ₹1,500 (Diploma) monthly | Monthly stipend to verified unemployed youth | **Delivered / Active** |
| **Shakti** | Transport Dept (G.O. TD 59 TRM 2023) | 100% free bus travel for women | Zero-fare passenger tickets & state reimbursements | **Delivered / Active** (Over 250+ crore trips logged) |

---

## 11. Production Deployment Guide

### Option A: Production WSGI Server (Waitress / Gunicorn)
Flask's built-in development server (`app.run()`) is single-threaded. For production, run with a WSGI server:

- **Windows / Cross-Platform (Waitress):**
  ```powershell
  waitress-serve --port=5000 wsgi:app
  ```
- **Linux / Cloud (Gunicorn):**
  ```bash
  gunicorn -w 4 -b 0.0.0.0:5000 wsgi:app
  ```

### Option B: Cloud Hosting (e.g., Render, Railway, AWS Lightsail)
1. Push the code to a private or public GitHub repository (ensuring `.env` is ignored by `.gitignore`).
2. Create a new **Web Service** on Render or Railway.
3. Set the build command: `pip install -r requirements.txt`.
4. Set the start command: `gunicorn wsgi:app`.
5. Add your database environment variables (`DB_HOST`, `DB_USER`, `DB_PASSWORD`, `DB_NAME`) in the hosting platform's Environment Settings.

---

## 12. Future Roadmap

- [ ] **State Expansion**: Compile verified manifesto and budget records for Tamil Nadu, Telangana, and Maharashtra.
- [ ] **React Frontend**: Migrate UI components to React.js while consuming the identical `/api/...` REST endpoints.
- [ ] **Government Budget Cross-Referencing**: Link scheme allocations directly to annual state budget speeches and Comptroller and Auditor General (CAG) reports.
- [ ] **Community Source Submission**: Allow verified researchers to submit departmental gazettes for peer review before publishing.

---

## 13. License

This project is licensed under the MIT License — see the [LICENSE](LICENSE) file for details. Built for educational and civic-accountability purposes.
