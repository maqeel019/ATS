import os
import re
from contextlib import suppress
from config import LOG_DIR
from extractor.section_segmenter import segment_sections


def sanitize_filename(name):
    """Replace unsafe characters for filenames with underscores."""
    return re.sub(r"[^\w\-\.]", "_", name)


def log_candidate_score(
    candidate,
    exp_score,
    skill_score,
    skill_matches,
    edu_score,
    profile_score,
    score,
    exp_method="",
    full_text="",
    pdf_filename="unknown.pdf",
    log_dir=LOG_DIR
):
    """
    Save candidate score + segmented sections + raw text.
    """
    os.makedirs(log_dir, exist_ok=True)

    base_name = os.path.splitext(os.path.basename(pdf_filename))[0]
    safe_name = sanitize_filename(base_name)

    # === Log file path ===
    log_file_path = os.path.join(log_dir, f"{safe_name}_score.txt")

    with suppress(Exception):
        with open(log_file_path, "w", encoding="utf-8") as f:
            f.write(f"PDF Filename: {pdf_filename}\n")
            f.write(f"Name (Extracted): {candidate.get('Name', 'unknown')}\n")
            f.write(f"Experience Score: {exp_score:.2f}\n")
            f.write(f"Skill Score: {skill_score:.2f} (Matched: {', '.join(skill_matches)})\n")
            f.write(f"Education Score: {edu_score:.2f}\n")
            f.write(f"Profile Score: {profile_score:.2f}\n")
            f.write(f"Total Score: {score:.2f}\n")
            f.write(f"Experience Extraction Method: {exp_method}\n")

            f.write("\n===== SEGMENTED SECTIONS =====\n")
            sections = segment_sections(full_text)
            for sec, content in sections.items():
                f.write(f"\n--- {sec.upper()} ---\n")
                f.write(content.strip() + "\n")

            f.write("\n===== RAW EXTRACTED TEXT =====\n")
            f.write(full_text.strip() + "\n")

    return round(score, 2)
