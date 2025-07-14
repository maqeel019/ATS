# 🧠 ATS Version 1.0 – Intelligent Resume Filtering System

A smart **Applicant Tracking System (ATS)** designed to parse, extract, rank, and filter PDF resumes using keyword matching, profile completeness, and text analysis. Built to handle thousands of CVs — even those with complex or non-ATS-friendly layouts.
---
## 🚀 Features
- 📄 Extract text from scanned or structured PDFs using:
  - `pdfplumber` (layout-aware text extraction)
  - `PyMuPDF` (`fitz`) for reliable text layer reading
  - `pdfminer.six` for fallback or additional structured extraction
  - OCR fallback with `pytesseract` + `pdf2image` for scanned images

- 🔍 Robust Information Extraction:
  - Name, Email, Phone
  - LinkedIn, GitHub
  - Skills (auto-extracted from text, supports comma/pipe/semicolon-separated formats)
  - Calculate total work experience from both:
        Explicit sentences ("4+ years of experience")
        Job timelines ("May 2021 — Apr 2022")
  - Education (raw & filtered highest degree)

- 📊 Smart Scoring & Ranking:
  - Experience Score
  - Skill Match Score
  - Education Score
  - Profile Completeness Score

- 🔎 Flexible Candidate Filtering:
  - `REQUIRED_SKILLS`
  - `MIN_EDUCATION`
  - `MIN_EXPERIENCE`

- ⚙️ Configurable Scoring & Filtering:
  - All filters and scoring weights are adjustable via config.py
  - Recruiters can tweak criteria without touching core logic

- 📥 Resume Input Handling:
  - Supports thousands of PDFs inside `/candidates/`
  - Handles structured and non-ATS-friendly resumes

- 📤 Output Reports:
  - `all_candidates.xlsx` — complete list
        - Filename	Name	Email	Phone	LinkedIn	GitHub	Skills	Experience	Education	RawEducation	Score Rank														
  - `filtered_candidates.xlsx` — only matching candidates
        - Name	Email	Phone	LinkedIn	GitHub	MatchedSkills	Experience	RawEducation	Education	Score	Rank	MissingSkills

- 📂 Logging for debugging purposes:
  - Each candidate gets a `logs/{name}_score.txt` with:
    - Scores (experience, skills, education, profile)
    - Extracted raw text from their PDF
```bash
## 📁 Folder Structure
ATS/
│
├── candidates/                  # Folder containing all resume PDFs
│
├── extractor/                  # Resume content & metadata extraction
│   ├── education.py
<<<<<<< HEAD
=======
│   ├── experience.py
>>>>>>> 9a7d7ab (enhanced version of ATS,two logs file:one for just raw texts another for segmented sections)
│   ├── info_extractor.py
│   ├── pdf_reader.py
│   ├── section_segmenter.py
│   └── __init__.py
│
├── scoring/                    # Scoring and filtering logic
│   ├── scoring.py
│   ├── filter.py
│   ├── log_candidate.py
│   └── __init__.py
│
├── utils/                      # Utility functions
│   ├── common.py
│   ├── file_utils.py
│   └── __init__.py
│
├── output/                     # Output results (Excel + Logs)
│   ├── all_candidates_ranked.xlsx
│   ├── filtered_candidates.xlsx
│   └── logs/                   # Text logs for each candidate
│
├── config.py                   # Global config for filters, skill sets, etc.
├── main.py                     # Main pipeline entry point
├── requirements.txt            # Python dependencies
├── README.md                   # Project documentation
└── __pycache__/                # Compiled Python cache files
```


## 🔧 Setup Instructions
### 1. Clone the repo

```bash
git clone https://github.com/maqeel019/ATS
cd ATS
2. Install dependencies
⚠️ Python ≥ 3.8 required

pip install -r requirements.txt
If using OCR features:

Install Tesseract OCR engine:

sudo apt install tesseract-ocr
For pdf2image:

sudo apt install poppler-utils


🛠️ How to Use
Add Resumes
Place all resume PDFs inside the candidates/ folder.

Run the Program
From the project root, run:
  python main.py
  View Output in the output/ folder:

📄 all_candidates.xlsx – all processed resumes with extracted data

🎯 filtered_candidates.xlsx – only candidates who meet your custom filters (skills, education, experience)

📝 logs/{name}_score.txt – per-candidate score breakdown and raw resume text for debugging



⚙️ Configuration
You can customize the scoring and filtering behavior by modifying the config.py file:

🎯 Recruiter Filters
Parameter   	                     Description	                                            Example
MIN_EXPERIENCE	      Minimum required experience (in years)	                              0.5
MIN_SCORE	            Minimum total score to pass filter	                                  60
REQUIRED_SKILLS     	Skills candidate must have	                                          {"python", "mysql", "power bi"}
MIN_EDUCATION	        Accepted degrees (lowercased match)	                                  {"bachelor", "master", "phd"}

🧠 Scoring Weights
Customize how the final score is calculated using:

RANKING_WEIGHTS = {
    "experience": 30,   # % weight for experience
    "skills": 40,       # % weight for skill match
    "education": 20,    # % weight for education level
    "profiles": 10      # % for Email,LinkedIn, GitHub,phoneNumber.
}

📁 File & Folder Paths
Change I/O paths if needed:

PDF_FOLDER              = "candidates/"                     # Folder containing PDF resumes
OUTPUT_DIR              = "output/"                         # Main output directory
OUTPUT_ALL_EXCEL        = "output/all_candidates_ranked.xlsx"
OUTPUT_FILTERED_EXCEL   = "output/filtered_candidates.xlsx"
LOG_DIR                 = "output/logs/"                    # Per-candidate logs

🧪 Skill Matching
The DEFAULT_SKILL_SET contains a wide list of industry skills used during skill extraction. You can:
Trim/extend it to match your domain (Data Science, DevOps, Web, etc.)
