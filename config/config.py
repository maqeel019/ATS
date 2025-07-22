# config.py
import os
# Debug settings
DEBUG_TEXT_OUTPUT = True

# Recruiter-defined parameters
MIN_EXPERIENCE        = 3.0    # minimum experience in years
MIN_SCORE             = 70     # minimum score threshold

MIN_EDUCATION         = {"bachelor", "master", "phd"}

REQUIRED_SKILLS = {
    "react",
    "javascript",
    "html",
    "API's Integration",
    "Material UI",
    "react.js",
    "css",
    "tailwind css",
    "typescript",
    "redux",
    "react router",
    "rest api",
    "git"
}

# === Base dir is the ATS/ root ===
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# === Where outputs go ===
OUTPUT_DIR = os.path.join(BASE_DIR, "output")
LOG_DIR = os.path.join(OUTPUT_DIR, "logs")

# === Where input PDFs go ===
PDF_FOLDER = os.path.join(BASE_DIR, "candidates")

# === Output Excel files ===
OUTPUT_ALL_EXCEL = os.path.join(OUTPUT_DIR, "all_candidates_ranked.xlsx")
OUTPUT_FILTERED_EXCEL = os.path.join(OUTPUT_DIR, "filtered_candidates.xlsx")


# Scoring weights
RANKING_WEIGHTS       = {
    "experience": 30,
    "skills": 40,
    "education": 20,
    "profiles": 10
}

# Month map for date parsing
_MONTH_MAP = {
    "january": 1, "jan": 1, "jan.": 1,
    "february": 2, "feb": 2, "feb.": 2,
    "march": 3, "mar": 3, "mar.": 3,
    "april": 4, "apr": 4, "apr.": 4,
    "may": 5,
    "june": 6, "jun": 6, "jun.": 6,
    "july": 7, "jul": 7, "jul.": 7,
    "august": 8, "aug": 8, "aug.": 8,
    "september": 9, "sep": 9, "sept": 9, "sep.": 9, "sept.": 9,
    "october": 10, "oct": 10, "oct.": 10,
    "november": 11, "nov": 11, "nov.": 11,
    "december": 12, "dec": 12, "dec.": 12,
}



# Degree ranking
_DEGREE_KEYWORDS = {
    "phd": 4,
    "doctor": 4,
    "master": 3,
    "m.sc": 3,
    "msc": 3,
    "mba": 3,
    "mca": 3,
    "m.s.": 3,
    "m.s.c": 3,
    "m.tech": 3,
    "m.e.": 3,
    "bachelor's": 2,
    "bachelor of science": 2,
    "bachelor of arts": 2,
    "bachelor of engineering": 2,
    "bachelor of technology": 2,
    "bachelor of computer applications": 2,
    "bachelor of computer science": 2,
    "bachelor of business administration": 2,
    "bachelor of commerce": 2,
    "bachelor of science in computer science": 2,
    "bachelor of science in information technology": 2,
    "bachelor of science in information systems": 2,
    "bachelor of science in software engineering": 2,
    "bachelor of science in data science": 2,
    "bachelor of science in artificial intelligence": 2,
    "bachelor of science in machine learning": 2,
    "bachelor of science in cybersecurity": 2,
    "bachelor of science in cloud computing": 2,
    "bachelor": 2,
    "b.sc": 2,
    "bsc": 2,
    "bs": 2,
    "bca": 2,
    "b.tech": 2,
    "ba": 2,
    "be": 2,
    "b.e.": 2,
    "b.e": 2,
    "diploma": 1,
    "polytechnic": 1,
    "high school": 0,
    "higher school": 0,
    "hsc": 0,
    "ssc": 0,
    "intermediate": 0,
    "12th": 0,
    "10th": 0,
}


