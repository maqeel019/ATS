import os
import pandas as pd
def load_resumes_from_folder(folder_path):
    return [
        os.path.join(folder_path, fn)
        for fn in os.listdir(folder_path)
        if fn.lower().endswith(".pdf")
    ]


def save_to_excel(df, output_path):
    df = df.sort_values(by="Score", ascending=False).reset_index(drop=True)
    df["Rank"] = df.index + 1
    df.to_excel(output_path, index=False)
    print(f"✅ Saved {len(df)} candidates to {output_path}")

