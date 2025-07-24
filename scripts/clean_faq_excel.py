import pandas as pd
import json
import os

# === Step 1: Load Excel ===
excel_path = "data/raw/Assessment and EC FAQs 22.5.25.xlsx"
df = pd.read_excel(excel_path, sheet_name="All FAQs with content column.")

# Keep only the relevant columns
df = df[["Title", "Content", "Subject"]].copy()
df.dropna(subset=["Title", "Content"], inplace=True)
df = df[df["Title"].str.strip() != ""]
df = df[df["Content"].str.strip() != ""]

# === Step 2: Filter by Relevance ===
KEYWORDS = [
    "extenuating", "assessment", "extension", "deadline", "claim",
    "support", "evidence", "illness", "exam", "reassessment",
    "resit", "certification", "mitigation", "panel", "submit"
]

def is_relevant_faq(title, content):
    combined = f"{title} {content}".lower()
    return any(kw in combined for kw in KEYWORDS)

df = df[df.apply(lambda row: is_relevant_faq(row["Title"], row["Content"]), axis=1)]

# === Step 3: Clean Text ===
df["Title"] = df["Title"].str.replace(r"\s+", " ", regex=True).str.strip()
df["Content"] = df["Content"].str.replace(r"\s+", " ", regex=True).str.strip()

# === Step 4: Save Outputs ===
os.makedirs("data/structured", exist_ok=True)

# Save as structured JSON
faq_json = df.to_dict(orient="records")
with open("data/structured/faq_cleaned.json", "w", encoding="utf-8") as f:
    json.dump(faq_json, f, indent=2, ensure_ascii=False)

# Save as instruction-output JSONL
with open("data/structured/faq_cleaned.jsonl", "w", encoding="utf-8") as f:
    for _, row in df.iterrows():
        example = {
            "instruction": row["Title"],
            "input": "",
            "output": row["Content"]
        }
        f.write(json.dumps(example, ensure_ascii=False) + "\n")

print(f"Cleaned FAQ saved as JSON and JSONL.")
print(f"Total relevant entries: {len(df)}")
