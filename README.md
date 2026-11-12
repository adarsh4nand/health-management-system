# 🌿 HealthTrack: Health and Wellness Awareness System

**A comprehensive digital platform designed to promote health literacy, track daily wellness habits, and provide AI-driven personalized insights for students and local communities.**

![Python](https://img.shields.io/badge/Python-3.10+-blue?logo=python)
![Flask](https://img.shields.io/badge/Flask-2.3.2-black?logo=flask)
![Scikit-Learn](https://img.shields.io/badge/ML-Scikit_Learn-orange?logo=scikit-learn)
![License](https://img.shields.io/badge/License-MIT-green)

---

## 📖 Project Overview
Many individuals, especially students and community members, lack awareness of fundamental health practices, leading to poor lifestyle choices and deteriorating well-being. **HealthTrack** bridges this gap by providing a lightweight, accessible, and intelligent web application that educates users, tracks their daily habits, and offers personalized, AI-generated wellness recommendations. 

This project was developed as a **B.Tech CSE Community Service Project** to demonstrate how technology can be leveraged for social good and digital health inclusion.

---

## ✨ Key Features

### 🧠 AI & Machine Learning Integration
- **AI Wellness Scoring:** An automated algorithm analyzes logged data (Water, Sleep, Exercise) against medical goals to generate an objective Wellness Score (1-10).
- **Personalized Video Recommendations:** Uses a Decision Tree Classifier (Scikit-Learn) to analyze user habits and dynamically recommend specific educational YouTube videos based on their weak points.
- **Dynamic Goal Calculation:** Calculates personalized daily water intake goals based on the user's body weight using medical formulas.

### 📊 Tracking & Analytics
- **Interactive Dashboard:** Visualizes weekly progress using **Chart.js** with a modern, responsive UI.
- **Historical Data Log:** Maintains a timestamped record of all user activities.
- **Data Portability:** One-click **CSV Export** feature allowing users or community health workers to download data for offline review.
- **Gamification:** Tracks and displays "Wellness Streaks" to encourage long-term habit formation.

### 🌍 Community & Awareness
- **Community Impact Dashboard:** Displays anonymized, aggregate data (e.g., average community sleep/water intake) to track campus-wide health trends.
- **Local Resource Directory:** A curated list of free/affordable local health camps, helplines, and yoga centers.
- **Myth vs. Fact Feed:** An educational section dedicated to busting common health misconceptions.

### 📱 Modern Web Capabilities
- **Progressive Web App (PWA):** Installable on mobile devices for a native app-like experience without Play Store dependency.
- **Automated Reminders:** UI integration for proactive daily wellness email reminders.
- **Cyberpunk/Tech UI:** A highly engaging, dark-mode, neon-accented user interface.

---

## 🛠️ Tech Stack

| Category | Technologies Used |
| :--- | :--- |
| **Frontend** | HTML5, CSS3, JavaScript, Chart.js |
| **Backend** | Python, Flask |
| **Database** | SQLite (Embedded for portability & serverless deployment) |
| **AI / ML** | Python Pandas, Scikit-Learn (Decision Tree Classifier) |
| **Deployment** | Vercel (Serverless Architecture) |

---

## 🚀 Installation & Local Setup

Follow these exact steps to run the project locally on your machine.

### Prerequisites
- **Python 3.10 or higher** installed on your system.
- **Git** installed (optional, but recommended for cloning).

### Step 1: Clone the Repository
Open your terminal or command prompt and run:
```bash
git clone https://github.com/your-username/health-management-system.git
cd health-management-system