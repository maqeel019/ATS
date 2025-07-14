from extractor.info_extractor import extract_matched_skills, extract_missing_skills

def apply_filtering(
    df,
    required_skills,
    min_experience,
    min_education,
    min_score,
    output_filtered_excel,
):
    
    
    # filtered_df = df[df["Score"] >= MIN_SCORE]  # Only keep candidates with score >= 70
    
    # Education filtering
    # filtered_df = df[df["Education"].isin(min_education)]     
    
    # Filter by score
    filtered_df = df[df["Experience (Years)"] >= min_experience]  # Only keep candidates with score >= min_score
    



    required_skills_lower = {skill.lower().strip() for skill in required_skills}

    filtered_df["Matched Skills"] = filtered_df["Skills"].apply(
    lambda s: extract_matched_skills(s, required_skills)
    )

    filtered_df["Missing Skills"] = filtered_df["Skills"].apply(
        lambda s: extract_missing_skills(s, required_skills)
    )


    filtered_df.to_excel(
        output_filtered_excel,
        index=False,
        columns=[
            "Name",
            "Email",
            "Phone",
            "LinkedIn",
            "GitHub",
            "Matched Skills",
            "Experience",
            # "Raw Education",
            "Education",
            "Score",
            "Rank",
            "Missing Skills",
        ],
    )
    print(f"✅ Filtered candidates saved to {output_filtered_excel}")

