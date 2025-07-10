import pandas as pd
import json

# Load Excel file
df = pd.read_excel("data/assessment_ec_faqs.xlsx")

# Rename columns for convenience
df = df.rename(columns={
    "Title": "student_query",
    "Content": "response"
})

# Drop rows with missing question or answer
df = df.dropna(subset=["student_query", "response"])

# 🧠 Rule-based label assignment (update as needed)
def label_query(query):
    q = str(query).lower()
    if "wellbeing" in q or "mental" in q or "supporting evidence for anxiety" in q:
        return "wellbeing_support"
    elif "support plan" in q or "reasonable adjustments" in q or "disability" in q:
        return "support_plan"
    elif "extension" in q or "illness" in q or "deadline" in q or "EC" in q:
        return "ec_extension"
    else:
        return "unknown"

# Apply labels
df["label"] = df["student_query"].apply(label_query)

# Save to JSON
records = df[["student_query", "label", "response"]].to_dict(orient="records")
with open("data/training_data.json", "w", encoding="utf-8") as f:
    json.dump(records, f, indent=2, ensure_ascii=False)

# Save to CSV for inspection
df[["student_query", "label", "response"]].to_csv("data/training_data.csv", index=False)

print(f"✅ Saved {len(df)} labeled examples to training_data.json and training_data.csv.")
