from extractor.info_extractor import extract_matched_skills, extract_missing_skills ,extract_skills
import re
def apply_filtering(
    df,
    required_skills,
    min_experience,
    min_education,
    min_score,
    output_filtered_excel,
):
    
        # Score filtering
    # filtered_df = df[df["Score"] >= MIN_SCORE].copy() 
    
        # Education filtering
    # filtered_df = df[df["Education"].isin(min_education)].copy()
    
        # Min Experince Filtering
    filtered_df = df[df["Experience (Years)"] >= min_experience].copy()
    
        # Skills filtering (Only candidates who has all required skills)
    # filtered_df = df[
    #     df["Skills"].apply(
    #         lambda s: set(required_skills).issubset(
    #             set(x.strip().lower() for x in re.split(r"[,\|;]+", s))
    #         )
    #     )
    # ].copy()


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

