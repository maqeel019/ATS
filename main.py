import os
import pandas as pd
from tqdm import tqdm
from scoring.scoring import assign_scores_and_ranks
from extractor.education import extract_highest_education, map_to_standard_degree
from extractor.info_extractor import extract_candidate_info, extract_links_from_pdf
from extractor.pdf_reader import (
    extract_text_pdfplumber,
    extract_text_fitz,
    extract_text_ocr,
    extract_text_pdfminer_wrapper,
)
from config.config import (
    MIN_EDUCATION,
    PDF_FOLDER,
    OUTPUT_ALL_EXCEL,
    OUTPUT_FILTERED_EXCEL,
    MIN_EXPERIENCE,
    REQUIRED_SKILLS,
    MIN_SCORE,
    LOG_DIR,
)
from config.skills_config import DEFAULT_SKILL_SET
from utils.file_utils import load_resumes_from_folder, save_to_excel
from utils.common import update_links
from extractor.experience import extract_experience
from scoring.filter import apply_filtering


def extract_and_save_candidate_info_to_excel(
    pdf_folder=PDF_FOLDER,
    output_all_excel=OUTPUT_ALL_EXCEL,
    output_filtered_excel=OUTPUT_FILTERED_EXCEL,
    skill_set=DEFAULT_SKILL_SET,
    required_skills=REQUIRED_SKILLS,
    min_experience=MIN_EXPERIENCE,
    min_education=MIN_EDUCATION,
    min_score=MIN_SCORE,
):
    rows = []
    os.makedirs(LOG_DIR, exist_ok=True)

    pdf_paths = load_resumes_from_folder(pdf_folder)

    for path in tqdm(pdf_paths, desc="Processing resumes", unit="file"):
        fn = os.path.basename(path)

        texts = []
        method_results = {}

        for label, func in [
            ("[EXTRACT_TEXT_PDFPLUMBER]", extract_text_pdfplumber),
            ("[EXTRACT_TEXT_FITZ]", extract_text_fitz),
            ("[EXTRACT_TEXT_PDFMINER_WRAPPER]", extract_text_pdfminer_wrapper),
        ]:
            t = func(path)
            if t and len(t.split()) > 50:
                method_results[label] = t
                texts.append(t)

        if not method_results:
            ocr_text = extract_text_ocr(path)
            method_results["[EXTRACT_TEXT_OCR]"] = ocr_text
            text = ocr_text
        else:
            text = "\n".join(texts)

        embedded_links = extract_links_from_pdf(path)
        info = extract_candidate_info(text, skill_set, filename=fn)
        info = update_links(info, embedded_links)

        years, months, method_type, pattern_used = extract_experience(text)
        total_exp = round(years + months / 12.0, 1)

        raw_education = extract_highest_education(text)
        standard_education = map_to_standard_degree(raw_education)

        rows.append(
            {
                "Filename": fn,
                "Name": info["name"],
                "Email": info["email"],
                "Phone": info["phone"],
                "LinkedIn": info["linkedin"],
                "GitHub": info.get("github", ""),
                "Skills": ", ".join(info["skills"]),
                "Experience": f"{years} years {months} months",
                "Experience (Years)": total_exp,
                "Education": standard_education,
                "Raw Education": raw_education,
                "Experience Method": f"{method_type} via {pattern_used}",
                "Text": text,
            }
        )

    if not rows:
        print("⚠️ No candidates found, nothing to save.")
        return

    df = pd.DataFrame(rows)
    df = assign_scores_and_ranks(df, required_skills, min_education, min_experience)

    if "Text" in df.columns:
        df.drop(columns=["Text"], inplace=True)

    save_to_excel(df, output_all_excel)
    os.makedirs(os.path.dirname(output_filtered_excel), exist_ok=True)
    apply_filtering(df, required_skills, min_experience, min_education, min_score, output_filtered_excel)


if __name__ == "__main__":
    extract_and_save_candidate_info_to_excel()
