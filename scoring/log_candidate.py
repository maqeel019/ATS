import os
import re
from contextlib import suppress
from config import LOG_DIR
<<<<<<< HEAD
from extractor.section_segmenter import segment_sections  #

def sanitize_filename(name):
    # Replace unsafe characters with underscore
    return re.sub(r"[^\w\-\.]", "_", name)

def log_candidate_score(candidate, exp_score, skill_score, skill_matches, edu_score,
                        profile_score, score, exp_method="", full_text="",
                        pdf_filename="unknown.pdf", log_dir=LOG_DIR):

    os.makedirs(log_dir, exist_ok=True)

    # Use the PDF file name (without .pdf) as the base for the log file name
=======
# from extractor.section_segmenter import segment_sections  #


def sanitize_filename(name):
    """Replace unsafe characters for filenames with underscores."""
    return re.sub(r"[^\w\-\.]", "_", name)

def log_candidate_score(candidate, exp_score, skill_score, skill_matches, edu_score,
                        profile_score, score, exp_method="",
                        full_text="", pdf_filename="unknown.pdf", log_dir=LOG_DIR):
    """
    Write raw extracted resume text + scoring info to a .txt file.
    Does NOT segment the text. Keeps 100% of extracted content.
    """
    os.makedirs(log_dir, exist_ok=True)

    # Clean and build safe file name
>>>>>>> 9a7d7ab (enhanced version of ATS,two logs file:one for just raw texts another for segmented sections)
    base_name = os.path.splitext(os.path.basename(pdf_filename))[0]
    safe_name = sanitize_filename(base_name)
    filename = os.path.join(log_dir, f"{safe_name}.txt")

<<<<<<< HEAD
    with suppress(Exception):  # Avoid crash if one file fails
=======
    with suppress(Exception):
>>>>>>> 9a7d7ab (enhanced version of ATS,two logs file:one for just raw texts another for segmented sections)
        with open(filename, "w", encoding="utf-8") as f:
            f.write(f"PDF Filename: {pdf_filename}\n")
            f.write(f"Name (Extracted): {candidate.get('Name', 'unknown')}\n")
            f.write(f"Experience Score: {exp_score:.2f}\n")
            f.write(f"Skill Score: {skill_score:.2f} (Matched: {', '.join(skill_matches)})\n")
            f.write(f"Education Score: {edu_score:.2f}\n")
            f.write(f"Profile Score: {profile_score:.2f}\n")
            f.write(f"Total Score: {score:.2f}\n")
            f.write(f"Experience Extraction Method: {exp_method}\n")
<<<<<<< HEAD
            
            f.write("\n===== Extracted Resume Text =====\n")
            sections = segment_sections(full_text)
            for section, content in sections.items():
                f.write(f"\n--- {section.upper()} ---\n")
                f.write(content.strip() + "\n")
=======

            f.write("\n===== RAW EXTRACTED RESUME TEXT =====\n")
            f.write(full_text.strip() + "\n")

>>>>>>> 9a7d7ab (enhanced version of ATS,two logs file:one for just raw texts another for segmented sections)
    return round(score, 2)
