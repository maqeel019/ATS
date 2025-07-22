import re
from scoring.log_candidate import log_candidate_score
from extractor.experience import extract_experience
from config.config import LOG_DIR, MIN_EXPERIENCE


def calculate_score(
    candidate,
    required_skills,
    preferred_education,
    min_experience=1,
    full_text="",
    years=None,
    months=None,
    exp_method="",
    pattern_used="",
    log_dir="logs"
):
    score = 0.0

    # --- 1. Experience Score ---
    if years is None or months is None:
        # fallback if not pre-passed
        from extractor.experience import extract_experience
        years, months, exp_method, pattern_used = extract_experience(
            candidate.get("Text", ""),
        )

    total_exp = years + months / 12.0
    exp_score = min(total_exp / min_experience, 1.0) * 30
    score += exp_score

    # --- 2. Skill Match Score ---
    raw = candidate.get("Skills", "")
    if isinstance(raw, str):
        tokens = re.split(r"[,\|;]+", raw)
        candidate_skills = set(tok.lower().strip() for tok in tokens if tok.strip())
    elif isinstance(raw, list):
        candidate_skills = set(s.lower().strip() for s in raw)
    else:
        candidate_skills = set()

    required_skills_lower = {s.lower().strip() for s in required_skills}
    skill_matches = candidate_skills & required_skills_lower

    skill_score = len(skill_matches) / len(required_skills_lower) * 40
    score += skill_score

    # --- 3. Education Score ---
    candidate_edu = candidate.get("Education", "").lower()
    edu_score = 20 if any(pref in candidate_edu for pref in preferred_education) else 10
    score += edu_score

    # --- 4. Profile Completeness ---
    profile_score = 0
    if candidate.get("Email"):
        profile_score += 3
    if candidate.get("Phone"):
        profile_score += 2
    if candidate.get("LinkedIn"):
        profile_score += 3
    if candidate.get("GitHub"):
        profile_score += 2
    score += profile_score

    # --- 5. Log files: raw + segmented ---
    log_candidate_score(
        candidate,
        exp_score, skill_score, skill_matches,
        edu_score, profile_score, score,
        exp_method=f"{exp_method} via {pattern_used}",
        full_text=full_text,
        pdf_filename=candidate.get("Filename", "unknown.pdf"),
        log_dir=log_dir
    )

    return round(score, 2)

def assign_scores_and_ranks(df, required_skills, min_education, min_experience):
    df["Score"] = df.apply(
        lambda row: calculate_score(
            row,
            required_skills,
            min_education,
            min_experience,
            full_text=row.get("Text", ""),
            years=row.get("Years"),
            months=row.get("Months"),
            exp_method=row.get("Experience Method", "").split(" via ")[0],
            pattern_used=row.get("Experience Method", "").split(" via ")[-1],
            log_dir=LOG_DIR
        ),
        axis=1,
    )
    df = df.sort_values(by="Score", ascending=False).reset_index(drop=True)
    df["Rank"] = df.index + 1
    return df

    df["Score"] = df.apply(
        lambda row: calculate_score(row, required_skills, min_education, min_experience,  full_text=row.get("Text", ""),log_dir=LOG_DIR  ),
        axis=1,
    )
    df = df.sort_values(by="Score", ascending=False).reset_index(drop=True)
    df["Rank"] = df.index + 1
    return df