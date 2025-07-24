import json
import re

# Load your structured JSON
with open("data/structured/nottingham_policies.json", "r", encoding="utf-8") as f:
    data = json.load(f)

# Define keywords → tags
TAG_KEYWORDS = {
    "evidence": ["evidence", "document", "proof", "certificate"],
    "assessment": ["assessment", "exam", "coursework", "test"],
    "self-certification": ["self-certify", "self-certification"],
    "deadline": ["deadline", "extension", "submission", "late"],
    "mental_health": ["mental health", "wellbeing", "counselling"],
    "panel": ["panel", "recommendation", "board of examiners"],
    "illness": ["illness", "sickness", "flu", "migraine", "health"],
    "bereavement": ["bereavement", "death", "loss"],
    "academic_misconduct": ["misconduct", "cheating", "plagiarism"],
}

def get_tags(text):
    text = text.lower()
    tags = set()
    for tag, keywords in TAG_KEYWORDS.items():
        if any(word in text for word in keywords):
            tags.add(tag)
    return list(tags)

# Enhance entries
for entry in data:
    content = entry.get("content", "")
    tags = get_tags(content)
    
    # Optional: rewrite 'Web Block 123' → First line of content
    if entry["section"].startswith("Web Block") or entry["section"].startswith("PDF Section"):
        first_line = content.split(".")[0].strip()
        if len(first_line) > 10:
            entry["section"] = first_line[:80] + ("..." if len(first_line) > 80 else "")

    entry["tags"] = tags

# Save enhanced data
with open("data/structured/nottingham_policies_tagged.json", "w", encoding="utf-8") as f:
    json.dump(data, f, indent=2, ensure_ascii=False)

print("Tags and section titles added. Saved to 'nottingham_policies_tagged.json'")
