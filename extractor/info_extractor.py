# extractor/info_extractor.py
import fitz  # PyMuPDF
import re
import os

<<<<<<< HEAD
def extract_name(text: str, filename: str = "") -> str:
    """
    Extracts the candidate's name from resume text, falling back to the filename if needed.
=======

def extract_name(text: str, filename: str = "") -> str:
    """
    Extracting the candidate's name from resume text, falling back to the filename if needed.
>>>>>>> 9a7d7ab (enhanced version of ATS,two logs file:one for just raw texts another for segmented sections)
    """
    lines = text.strip().splitlines()
    skip_keywords = re.compile(
        r"(email|@|\.com|http|linkedin|github|phone|contact|whatsapp|engineer|developer|certified|professionalexperience|professional|skills|education|experience|summary|profile|objective|interests|hobbies)",
        re.IGNORECASE
    )

<<<<<<< HEAD
    # 1. Heuristic scan of the first 10 lines
=======
    # 1.scan of the first 10 lines
>>>>>>> 9a7d7ab (enhanced version of ATS,two logs file:one for just raw texts another for segmented sections)
    for line in lines[:10]:
        line = line.strip()
        if not line or skip_keywords.search(line):
            continue

        # Accept lines with 2–4 alphabetic words that resemble names
        words = line.split()
        if 2 <= len(words) <= 4 and all(re.match(r"^[A-Za-z'-]+$", w) for w in words):
            return " ".join(w.capitalize() for w in words)

    # 2. Fallback: try parsing the name from the filename
    base = os.path.basename(filename)
    base = re.sub(r"\.(pdf|PDF)$", "", base)
    base = re.sub(r"^\d+[-_]", "", base)
<<<<<<< HEAD
    base = re.sub(r"[_\-]+", " ", base)  # Replace _ and - with spaces
=======
    base = re.sub(r"[_\-]+", " ", base)
>>>>>>> 9a7d7ab (enhanced version of ATS,two logs file:one for just raw texts another for segmented sections)
    base = re.sub(r"\b(cv|resume|profile)\b", "", base, flags=re.IGNORECASE)
    base = base.strip()

    # Keep only first 3–4 words
    name_parts = base.split()
    if 1 < len(name_parts) <= 5:
        return " ".join(w.capitalize() for w in name_parts)

    # 3. Last fallback
    return base.title()


<<<<<<< HEAD
=======
def extract_email(text):
    m = re.search(r"[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[A-Za-z]{2,}", text)
    if m:
        return m.group().strip().rstrip(".,;:")
    return ""


def extract_phone(text):
    m = re.search(r"\+?[\d\-\s()]{7,}\d", text)
    if m:
        raw = m.group()
        return re.sub(r"[^\d+]", "", raw).strip()
    return ""


def fix_broken_urls(text):
    text = re.sub(
        r"(linkedin\.com/in/)\s*\n*\s*([A-Za-z0-9_-]+)",
        r"\1\2",
        text,
        flags=re.IGNORECASE
    )
    text = re.sub(
        r"(github\.com/)\s*\n*\s*([A-Za-z0-9_.-]+)",
        r"\1\2",
        text,
        flags=re.IGNORECASE
    )
    return text


def extract_linkedin(text):
    for pat in [
        r"https?://(?:www\.)?linkedin\.com/in/[A-Za-z0-9_-]+",
        r"www\.linkedin\.com/in/[A-Za-z0-9_-]+",
        r"linkedin\.com/in/[A-Za-z0-9_-]+",
    ]:
        m = re.search(pat, text, re.IGNORECASE)
        if m:
            link = m.group(0)
            if not link.startswith("http"):
                link = "https://" + link.lstrip("/")
            return link
    return ""


def extract_github(text):
    for pat in [
        r"https?://(?:www\.)?github\.com/[A-Za-z0-9_.-]+",
        r"www\.github\.com/[A-Za-z0-9_.-]+",
        r"github\.com/[A-Za-z0-9_.-]+",
    ]:
        m = re.search(pat, text, re.IGNORECASE)
        if m:
            link = m.group(0)
            if not link.startswith("http"):
                link = "https://" + link.lstrip("/")
            return link
    return ""


>>>>>>> 9a7d7ab (enhanced version of ATS,two logs file:one for just raw texts another for segmented sections)
def extract_links_from_pdf(pdf_path):
    links = []
    doc = fitz.open(pdf_path)
    for page in doc:
        for link in page.get_links():
            uri = link.get("uri", "")
            if uri and ("linkedin.com" in uri or "github.com" in uri):
                links.append(uri)
    return links


def extract_skills(text, skill_set):
    found_skills = set()
    clean_text = text.lower()

    for skill in skill_set:
        words = skill.lower().split()
        pattern = r"\b" + r"\s+".join(re.escape(w) for w in words) + r"\b"
        if re.search(pattern, clean_text):
            found_skills.add(skill.lower())

    return list(found_skills)


<<<<<<< HEAD
def extract_candidate_info(text, skill_set , filename):
    """
    Extract basic candidate info: name, email, phone, linkedin, skills.
    Improved phone‐regex to only grab sequences of ≥7 digits, so we don’t catch
    the “67” in an email address.
    """
    info = {"name": "", "email": "", "phone": "", "linkedin": "", "skills": []}

    # 1) Heuristic for name: first line with 1–5 words, all letters/spaces.
    name = extract_name(text, filename)
    info["name"] = name

    # 2) Email extraction (unchanged)
    m = re.search(r"[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+[,\.][A-Za-z]{2,}", text)
    if m:
        email = m.group().replace(",", ".")  # fix common mistake
        info["email"] = email


    # 3) Phone extraction: only match sequences of at least 7 digits (with optional '+', spaces, dashes)
    m = re.search(r"\+?[\d\-\s()]{7,}\d", text)
    if m:
        # strip everything except digits and leading '+'
        raw = m.group()
        info["phone"] = re.sub(r"(?!^\+)[^\d]", "", raw)

    # 4) LinkedIn extraction (unchanged)
    for pat in [
        r"https?://(?:www\.)?linkedin\.com/in/[A-Za-z0-9_-]+",
        r"www\.linkedin\.com/in/[A-Za-z0-9_-]+",
        r"linkedin\.com/in/[A-Za-z0-9_-]+",
    ]:
        m = re.search(pat, text, re.IGNORECASE)
        if m:
            link = m.group(0)
            if not link.startswith("http"):
                link = "https://" + link
            info["linkedin"] = link
            break

    # 5) Skill matching (unchanged)
    info["skills"] = extract_skills(text, skill_set)

    return info


=======
>>>>>>> 9a7d7ab (enhanced version of ATS,two logs file:one for just raw texts another for segmented sections)
def extract_matched_skills(skill_text, required_skills):
    required_skills_lower = {skill.lower().strip()
                             for skill in required_skills}

    if isinstance(skill_text, str):
        skills = re.split(r"[,\|;:\n\t]+", skill_text)
        matched = [
            s.strip() for s in skills if s.strip().lower() in required_skills_lower
        ]
        return ", ".join(matched)
    return ""


def extract_missing_skills(skill_text, required_skills):
    required_skills_lower = {skill.lower().strip()
                             for skill in required_skills}

    if isinstance(skill_text, str):
        skills = re.split(r"[,\|;:\n\t]+", skill_text)
        present = {s.strip().lower() for s in skills}
        missing = [s for s in required_skills_lower if s not in present]
        return ", ".join(missing)
    return ", ".join(required_skills_lower)
<<<<<<< HEAD
=======


def fallback_embed_links(info, pdf_path):
    """
    If LinkedIn or GitHub is still missing, fallback to embedded PDF hyperlinks.
    """
    embedded_links = extract_links_from_pdf(pdf_path)
    unique_links = set(embedded_links)

    for link in unique_links:
        link_lower = link.lower()
        if "linkedin.com" in link_lower and not info["linkedin"]:
            info["linkedin"] = link
        if "github.com" in link_lower and not info["github"]:
            info["github"] = link


def extract_candidate_info(text, skill_set, filename, pdf_path=None):
    info = {
        "name": extract_name(text, filename),
        "email": extract_email(text),
        "phone": extract_phone(text),
        "linkedin": "",
        "github": "",
        "skills": []
    }

    text_fixed = fix_broken_urls(text)

    info["linkedin"] = extract_linkedin(text_fixed)
    info["github"] = extract_github(text_fixed)

    if pdf_path:
        fallback_embed_links(info, pdf_path)

    info["skills"] = extract_skills(text, skill_set)
    return info
>>>>>>> 9a7d7ab (enhanced version of ATS,two logs file:one for just raw texts another for segmented sections)
