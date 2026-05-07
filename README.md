# 🧭 Career Path Intelligence System

> An ML-powered career guidance web app that matches your skills to real job roles, identifies skill gaps, and generates a personalized learning roadmap.

**🔗 Live Demo → [career-path-intelligence-7ckgsdy43rttzzyochutk8.streamlit.app](https://career-path-intelligence-7ckgsdy43rttzzyochutk8.streamlit.app)**

---

## 📌 What It Does

Most career guidance tools tell you *what* jobs exist. This tells you *how close you are* — and exactly what to learn next.

You type your skills. The system:
1. **Matches** them against 42 real-world job roles using TF-IDF + Cosine Similarity
2. **Ranks** roles by compatibility percentage
3. **Detects** which skills you're missing for each role
4. **Generates** a prioritized learning roadmap with free course links

---

## 🖥️ Screenshots

| Landing Page | Match Results |
|---|---|
| ![Landing](screenshots/landing.png) | ![Results](screenshots/results.png) |

| Skill Gap Analysis | Learning Roadmap |
|---|---|
| ![Gap](screenshots/gap.png) | ![Roadmap](screenshots/roadmap.png) |

---

## ⚙️ Tech Stack

| Layer | Technology |
|---|---|
| Language | Python 3.11 |
| Web Framework | Streamlit |
| Machine Learning | Scikit-learn (TF-IDF + Cosine Similarity) |
| Data Processing | Pandas, NumPy |
| Visualizations | Plotly |
| Dataset | Kaggle — Job Description Dataset (1.6M rows) |
| Deployment | Streamlit Cloud |

---

## 🧠 How The ML Works

### Step 1 — Data Pipeline
Raw dataset of 1.6 million job postings is cleaned, normalized, and grouped by role. The top 15 most frequently required skills per role are extracted and saved to `data/job_roles.csv`.

### Step 2 — TF-IDF Vectorization
Each role's skill text is converted into a numerical vector using **TF-IDF (Term Frequency–Inverse Document Frequency)**. Skills that are specific to one role get high weight; generic words get low weight.

### Step 3 — Cosine Similarity Matching
The user's input is vectorized in the same space. **Cosine similarity** measures the angle between the user vector and every role vector. A smaller angle = higher match percentage.

### Step 4 — Keyword Gap Detection
Missing skills are identified by extracting the most meaningful keywords from a role's skill profile and checking which ones are absent from the user's input.

### Step 5 — Roadmap Generation
Missing keywords are mapped against a curated resource library of 40+ free courses (Coursera, freeCodeCamp, Google, AWS) and returned as a prioritized learning plan.

---

## 📁 Project Structure

```
career-path-intelligence/
├── app.py                  ← Streamlit UI entry point
├── data/
│   └── job_roles.csv       ← Cleaned dataset (42 roles)
├── utils/
│   ├── data_cleaner.py     ← Processes raw Kaggle dataset
│   ├── matcher.py          ← TF-IDF + Cosine Similarity engine
│   ├── gap_detector.py     ← Skill gap analysis
│   └── recommender.py      ← Learning roadmap generator
├── requirements.txt
└── README.md
```

---

## 🚀 Run Locally

### Prerequisites
- Python 3.11+
- pip

### Setup

```bash
# Clone the repository
git clone https://github.com/vishvrajsolanki-dev/career-path-intelligence.git
cd career-path-intelligence

# Create and activate virtual environment
python -m venv venv
venv\Scripts\activate        # Windows
source venv/bin/activate     # Mac/Linux

# Install dependencies
pip install -r requirements.txt

# Run the app
streamlit run app.py
```

The app opens at `http://localhost:8501`

### Dataset Note
The raw Kaggle dataset (`data/raw_jobs.csv`) is not included in this repository due to its size (1.6M rows). The cleaned output `data/job_roles.csv` is included and sufficient to run the app.

To regenerate from raw data:
1. Download from [Kaggle — Job Description Dataset](https://www.kaggle.com/datasets/ravindrasinghrana/job-description-dataset)
2. Place as `data/raw_jobs.csv`
3. Run `python utils/data_cleaner.py`

---

## 📊 Dataset

- **Source:** [Kaggle — Job Description Dataset](https://www.kaggle.com/datasets/ravindrasinghrana/job-description-dataset) by Ravindra Singh Rana
- **Raw size:** 1,615,940 rows × 23 columns
- **After cleaning:** 42 unique job roles with top 15 skills each
- **Key columns used:** `Job Title`, `skills`

---

## ✨ Features

- **Skill input** — Free text or comma-separated
- **Quick profiles** — One-click example skill sets (Data Science, Web Dev, Marketing)
- **Match score chart** — Horizontal bar chart ranked by compatibility %
- **Role cards** — Expandable per-role breakdown with progress bar
- **Skill badges** — Green (have) / Red (missing) visual indicators
- **Learning roadmap** — Clickable table with course name, platform, duration, link
- **Coverage chart** — Stacked bar showing skills gap across all matched roles
- **Sidebar controls** — Adjust number of roles shown, toggle roadmap

---

## 🗺️ Roadmap (Future Improvements)

- [ ] Semantic skill matching using `sentence-transformers`
- [ ] Resume PDF upload and auto-extraction of skills
- [ ] Salary range display per role
- [ ] User accounts to save progress over time
- [ ] Export roadmap as PDF

---

## 👤 Author

**Vishvrajsinh Solanki**
- GitHub: [@vishvrajsolanki-dev](https://github.com/vishvrajsolanki-dev)

---

## 📄 License

This project is open source and available under the [MIT License](LICENSE).

---

*Built as a portfolio project demonstrating applied machine learning, data engineering, and full-stack Python development.*