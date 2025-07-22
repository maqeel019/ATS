
# 🧠 ATS – Intelligent Resume Filtering System

A smart **Applicant Tracking System (ATS)** designed to parse, extract, rank, and filter PDF resumes using keyword matching, profile completeness, and text analysis. Built to handle thousands of CVs — even those with complex or non-ATS-friendly layouts.

---

## 🚀 Features

- 📄 **Advanced PDF Extraction:**
  - `pdfplumber` (layout-aware)
  - `PyMuPDF` (`fitz`) for text layer
  - `pdfminer.six` fallback
  - OCR fallback (`pytesseract` + `pdf2image`) for scanned images

- 🔍 **Robust Information Extraction:**
  - Name, Email, Phone
  - LinkedIn, GitHub
  - Skills (auto-extracted)
  - Calculate work experience from:
    - Explicit statements ("4+ years of experience")
    - Job timelines (date ranges)
  - Education (raw & highest degree)

- 📊 **Smart Scoring & Ranking:**
  - Experience Score
  - Skill Match Score
  - Education Score
  - Profile Completeness Score

- 🔎 **Flexible Candidate Filtering:**
  - REQUIRED_SKILLS
  - MIN_EDUCATION
  - MIN_EXPERIENCE
  - MIN_SCORE

- ⚙️ **Configurable & Extensible:**
  - All filters, paths, and skill sets in `config/config.py` and `config/skills_config.py`
  - Add or change skills easily for different hiring fields

- 📥 **Resume Input Handling:**
  - Drop thousands of PDFs in `/candidates/`
  - Handles ATS-friendly and messy resumes

- 📤 **Clear Output:**
  - `all_candidates_ranked.xlsx` — full processed list
  - `filtered_candidates.xlsx` — only qualified candidates

- 🗂️ **Detailed Logs:**
  - `logs/{name}_Raw.txt`: scores and raw text
  - `logs/{name}_Segmented.txt`: segmented text sections

---

## 📁 Folder Structure

```bash
ATS/
│
├── candidates/                 # All resume PDFs
│
├── extractor/                  # Extraction logic
│   ├── education.py
│   ├── experience.py
│   ├── info_extractor.py
│   ├── pdf_reader.py
│   ├── section_segmenter.py
│   └── **init**.py
│
├── scoring/                    # Scoring & filtering
│   ├── scoring.py
│   ├── filter.py
│   ├── log_candidate.py
│   └── **init**.py
│
├── utils/                      # Utilities
│   ├── common.py
│   ├── file_utils.py
│   └── **init**.py
│
├── config/                     # Config files
│   ├── config.py               # Global paths & thresholds And Configuration
│   ├── skills_config.py        # Master skill sets (tech, data, etc.)
│
├── output/                     # Excel & log outputs
│   ├── all_candidates_ranked.xlsx
│   ├── filtered_candidates.xlsx
│   └── logs/
│       ├── {Resume_name}_Raw.txt
│       └── {Resume_name}_Segmented.txt
│
├── main.py                     # Pipeline entry point
├── requirements.txt            # Python dependencies
├── README.md                   # Project docs
└── **pycache**/
```

---

## 🔧 Setup Instructions

### 1️⃣ Clone the Repo
```bash
git clone https://github.com/maqeel019/ATS
cd ATS
````

### 2️⃣ Install Dependencies

Python 3.8+

```bash
pip install -r requirements.txt
```

**If using OCR:**

```bash
sudo apt install tesseract-ocr
sudo apt install poppler-utils
```

---

## ⚙️ How to Use

### 📥 Add Resumes

Put all resume PDFs in the `candidates/` folder.

### ▶️ Run the Pipeline

```bash
python main.py
```

### 📊 View Results in `output/`

* `all_candidates_ranked.xlsx`: every processed resume
* `filtered_candidates.xlsx`: only resumes matching your filters
* `logs/{name}_Raw.txt`: raw text & scores
* `logs/{name}_Segmented.txt`: segmented sections

---

## 🛠️ Configuration

All settings are in `config/config.py` and `config/skills_config.py`.

| Parameter         | Description                                | Example                           |
| ----------------- | ------------------------------------------ | --------------------------------- |
| `MIN_EXPERIENCE`  | Minimum required experience (years)        | `0.5`                             |
| `MIN_SCORE`       | Minimum total score to pass filter         | `60`                              |
| `REQUIRED_SKILLS` | Required skills (matches extracted skills) | `{"python", "mysql", "power bi"}` |
| `MIN_EDUCATION`   | Minimum degree(s) accepted                 | `{"bachelor", "master", "phd"}`   |

### 🔢 Scoring Weights

```py
RANKING_WEIGHTS = {
    "experience": 30,  # %
    "skills": 40,      # %
    "education": 20,   # %
    "profiles": 10     # %
}
```

### 📦 File & Folder Paths

```py
PDF_FOLDER              = "candidates/"
OUTPUT_DIR              = "output/"
OUTPUT_ALL_EXCEL        = "output/all_candidates_ranked.xlsx"
OUTPUT_FILTERED_EXCEL   = "output/filtered_candidates.xlsx"
LOG_DIR                 = "output/logs/"
```

### 🧩 Skills Configuration

All core tech skills live in `config/skills_config.py` — you can:

* Expand with backend, data science, devops, etc.
* Keep separate skill sets for different roles
* Easily plug into your pipeline via `DEFAULT_SKILL_SET`

---