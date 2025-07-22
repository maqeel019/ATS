import re

def assign_scores_and_ranks(
    df,
    required_skills,
    min_education,
    min_experience,
    preferred_education=("bachelor", "master", "msc", "bsc"),
):
    """
    Scores candidates based on experience, skills, education, and profile completeness.
    Assumes:
      - 'Experience (Years)' exists.
      - 'Skills' is a list of lowercased skills.
    """

    scores = []

    required_skills_lower = {s.lower().strip() for s in required_skills}

    for _, candidate in df.iterrows():
        score = 0

        # --- 1. Experience Score ---
        total_exp = candidate.get("Experience (Years)", 0) or 0
        exp_score = min(total_exp / min_experience, 1.0) * 30
        score += exp_score

        # --- 2. Skill Match Score ---
        raw = candidate.get("Skills", [])
        if isinstance(raw, list):
            candidate_skills = set(s.strip() for s in raw)
        else:
            # Fallback if something slipped through
            tokens = re.split(r"[,\|;]+", str(raw))
            candidate_skills = set(tok.lower().strip() for tok in tokens if tok.strip())

        skill_matches = candidate_skills & required_skills_lower
        skill_score = len(skill_matches) / len(required_skills_lower) * 40
        score += skill_score

        # --- 3. Education Score ---
        candidate_edu = str(candidate.get("Education", "")).lower()
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
        score = round(score ,2)
        scores.append(score)

    df["Score"] = scores
    df = df.sort_values(by="Score", ascending=False).reset_index(drop=True)
    df["Rank"] = df.index + 1

    return df
