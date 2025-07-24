import json

# Load structured policy data
with open("data/structured/nottingham_policies_tagged_cleaned.json", "r", encoding="utf-8") as f:
    data = json.load(f)

# Convert to instruction-style format
with open("data/structured/policies_cleaned.jsonl", "w", encoding="utf-8") as out:
    for item in data:
        section = item.get("section", "").strip()
        content = item.get("content", "").strip()
        if not content or not section:
            continue
        instruction = f"What is the university guidance on: {section}?"
        out.write(json.dumps({
            "instruction": instruction,
            "input": "",
            "output": content
        }, ensure_ascii=False) + "\n")

print("Saved: policies_cleaned.jsonl")
