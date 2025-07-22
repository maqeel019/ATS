import os
import re
from contextlib import suppress
from config.config import LOG_DIR
from extractor.section_segmenter import post_process_sections, segment_sections


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
    Save candidate logs:
    1) Raw text file (.txt)
    2) Segmented sections (.txt)
    No score log here — score returned only.
    """
    os.makedirs(log_dir, exist_ok=True)

    base_name = os.path.splitext(os.path.basename(pdf_filename))[0]
    safe_name = sanitize_filename(base_name)

    # === Save raw text ===
    raw_txt_path = os.path.join(log_dir, f"{safe_name}_Raw.txt")
    with suppress(Exception):
        with open(raw_txt_path, "w", encoding="utf-8") as f:
            f.write(full_text)

    # === Save segmented text===
    sections = segment_sections(full_text)
    
    segmented_txt_path = os.path.join(log_dir, f"{safe_name}_Segmented.txt")
    with suppress(Exception):
        with open(segmented_txt_path, "w", encoding="utf-8") as f:
            for sec_name, sec_content in sections.items():
                f.write(f"\n===== {sec_name.upper()} =====\n")
                f.write(sec_content.strip())
                f.write("\n\n")

    return round(score, 2)
