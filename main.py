import os
import pandas as pd
from scoring.scoring import assign_scores_and_ranks
<<<<<<< HEAD
from extractor.education import (extract_highest_education,map_to_standard_degree)
from extractor.info_extractor import (extract_candidate_info , extract_links_from_pdf )
from extractor.pdf_reader import ( extract_text_pdfplumber , extract_text_fitz, extract_text_ocr ,extract_text_pdfminer_wrapper)
from config import DEFAULT_SKILL_SET, MIN_EDUCATION
from scoring.filter import apply_filtering
from config import (PDF_FOLDER , OUTPUT_ALL_EXCEL , OUTPUT_FILTERED_EXCEL,
                    MIN_EXPERIENCE, REQUIRED_SKILLS, MIN_SCORE , LOG_DIR )
from utils.file_utils import load_resumes_from_folder, save_to_excel
from utils.common import  update_links
=======
from extractor.education import extract_highest_education, map_to_standard_degree
from extractor.info_extractor import extract_candidate_info, extract_links_from_pdf
from extractor.pdf_reader import (
    extract_text_pdfplumber,
    extract_text_fitz,
    extract_text_ocr,
    extract_text_pdfminer_wrapper,
)
from extractor.section_segmenter import segment_sections
from config import DEFAULT_SKILL_SET, MIN_EDUCATION
from scoring.filter import apply_filtering
from config import (
    PDF_FOLDER,
    OUTPUT_ALL_EXCEL,
    OUTPUT_FILTERED_EXCEL,
    MIN_EXPERIENCE,
    REQUIRED_SKILLS,
    MIN_SCORE,
    LOG_DIR,
)
from utils.file_utils import load_resumes_from_folder, save_to_excel
from utils.common import update_links
>>>>>>> 9a7d7ab (enhanced version of ATS,two logs file:one for just raw texts another for segmented sections)
from extractor.experience import extract_experience


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
<<<<<<< HEAD

    # Ensure output directories exist /Loadinf resumes from folder
    for path in load_resumes_from_folder(pdf_folder):
        fn = os.path.basename(path)

        # Extract text (pdfplumber → PyMuPDF → OCR)
        texts = []

        for method in [extract_text_pdfplumber, extract_text_fitz, extract_text_pdfminer_wrapper]:
            t = method(path)
            if t and len(t.split()) > 50:
                texts.append(t)

        if not texts:
            text = extract_text_ocr(path)
        else:
            text = "\n".join(texts)


        embedded_links = extract_links_from_pdf(path)
         # Extract candidate information
        info = extract_candidate_info(text, skill_set ,filename=fn)
        
        # Update the info dictionary with embedded links
        info = update_links(info, embedded_links)

        # Build log path
        log_filename = f"{info['name'].lower().replace(' ', '_')}_score.txt"
        log_path = os.path.join(LOG_DIR, log_filename)

        # Extract experience in years and months
        years, months, method_type, pattern_used = extract_experience(text, log_path)
        total_exp = years + months / 12.0
        total_exp = round(total_exp, 1)  # Round to 2 decimal places
        
        # Extract highest education level and map to standard degree
=======
    os.makedirs(LOG_DIR, exist_ok=True)

    for path in load_resumes_from_folder(pdf_folder):
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

        # ✅ STEP 1 & 2 — Save raw extracted text to logs/<name>.txt
        log_filename_txt = fn.replace(".pdf", ".txt")
        log_path_txt = os.path.join(LOG_DIR, log_filename_txt)
        with open(log_path_txt, "w", encoding="utf-8") as f:
            f.write(text)
        # print(f"✅ Raw extracted text saved to: {log_path_txt}")

        # ✅ STEP 3 — Use log text as source for segmentation
        text_for_segmentation = text  # always fresh — we just wrote it

        sections = segment_sections(text_for_segmentation)

        # ✅ STEP 4 — Save sections into logs/<name>_segmented.txt
        combined_out_file = os.path.join(LOG_DIR, f"{os.path.splitext(fn)[0]}_segmented.txt")
        with open(combined_out_file, "w", encoding="utf-8") as f:
            for sec_name, sec_content in sections.items():
                f.write(f"\n===== {sec_name.upper()} =====\n")
                f.write(sec_content.strip())
                f.write("\n\n")

        # print(f"✅ Segmented text saved to: {combined_out_file}")

        # Continue normal extraction:
        embedded_links = extract_links_from_pdf(path)
        info = extract_candidate_info(text, skill_set, filename=fn)
        info = update_links(info, embedded_links)

        log_filename_score = f"{info['name'].lower().replace(' ', '_')}_score.txt"
        log_path = os.path.join(LOG_DIR, log_filename_score)
        years, months, method_type, pattern_used = extract_experience(text, log_path)
        total_exp = round(years + months / 12.0, 1)

>>>>>>> 9a7d7ab (enhanced version of ATS,two logs file:one for just raw texts another for segmented sections)
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
<<<<<<< HEAD
                "Education": standard_education,  # <- for filtering
                "Raw Education": raw_education,  
                "Experience Method": f"{method_type} via {pattern_used}",
                "Text": text
=======
                "Education": standard_education,
                "Raw Education": raw_education,
                "Experience Method": f"{method_type} via {pattern_used}",
                "Text": text,
>>>>>>> 9a7d7ab (enhanced version of ATS,two logs file:one for just raw texts another for segmented sections)
            }
        )

    if not rows:
        print("⚠️ No candidates found, nothing to save.")
        return

    df = pd.DataFrame(rows)
<<<<<<< HEAD
 
    # Calculate ranking score for all candidates
    df = assign_scores_and_ranks(df, required_skills, min_education, min_experience)
    
    # 2. Remove the "Text" column before saving
    if "Text" in df.columns:
         df.drop(columns=["Text"], inplace=True)
    # Save full ranked list
    save_to_excel(df, output_all_excel)

    # Call filtering function from filter.py
=======
    df = assign_scores_and_ranks(df, required_skills, min_education, min_experience)

    if "Text" in df.columns:
        df.drop(columns=["Text"], inplace=True)

    save_to_excel(df, output_all_excel)
>>>>>>> 9a7d7ab (enhanced version of ATS,two logs file:one for just raw texts another for segmented sections)
    os.makedirs(os.path.dirname(OUTPUT_FILTERED_EXCEL), exist_ok=True)
    apply_filtering(df, required_skills, min_experience, min_education, min_score, output_filtered_excel)


if __name__ == "__main__":
    extract_and_save_candidate_info_to_excel()
