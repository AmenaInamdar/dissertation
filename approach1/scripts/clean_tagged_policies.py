import json
import os

# Load tagged policy data
input_file = "data/structured/nottingham_policies_tagged.json"
output_file = "data/structured/nottingham_policies_tagged_cleaned.json"

with open(input_file, "r", encoding="utf-8") as f:
    data = json.load(f)

# Helper: check if content is useful policy text
def is_valid_policy_text(text):
    if not text or len(text.strip()) < 40:
        return False

    keywords = [
        "assessment", "extenuating", "evidence", "panel", "claim",
        "support", "illness", "certification", "self-certify", "deadline",
        "resit", "module", "exam", "coursework", "impact"
    ]
    text_lower = text.lower()
    return any(keyword in text_lower for keyword in keywords)

# Clean and rename entries
cleaned_data = []

for entry in data:
    content = entry.get("content", "").strip()
    if not is_valid_policy_text(content):
        continue  # Skip irrelevant or too-short content

    # Improve section name if generic
    section = entry.get("section", "")
    if section.startswith("Web Block") or section.startswith("PDF Section"):
        first_line = content.split("\n")[0].strip()
        if len(first_line) > 5:
            section = first_line[:80] + ("..." if len(first_line) > 80 else "")

    entry["section"] = section
    cleaned_data.append(entry)

# Save cleaned JSON
os.makedirs(os.path.dirname(output_file), exist_ok=True)
with open(output_file, "w", encoding="utf-8") as f:
    json.dump(cleaned_data, f, indent=2, ensure_ascii=False)

print(f"Cleaned data saved to: {output_file}")
print(f"Retained {len(cleaned_data)} clean, tagged entries.")
