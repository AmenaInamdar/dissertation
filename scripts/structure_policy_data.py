import json
import os

input_path = "data/policy_data.json"
output_path = "data/policy_structured.json"

# Simple mapping to match categories with readable titles
CATEGORY_TITLES = {
    "wellbeing": "Wellbeing Support",
    "extenuating_circumstances": "Extenuating Circumstances",
    "support_plans": "Support Plans"
}

def extract_summary_conditions_outcome(text):
    # Naive split based on typical sections — you can improve this manually later
    lines = text.split("\n")
    summary = []
    conditions = []
    outcome = []

    in_conditions = False
    in_outcome = False

    for line in lines:
        lower = line.lower()
        if "you must" in lower or "requirement" in lower or "should provide" in lower or "evidence" in lower:
            in_conditions = True
            in_outcome = False
        elif "you may receive" in lower or "outcome" in lower or "results in" in lower:
            in_conditions = False
            in_outcome = True

        if in_conditions:
            conditions.append(line.strip())
        elif in_outcome:
            outcome.append(line.strip())
        else:
            summary.append(line.strip())

    return {
        "summary": " ".join(summary[:5]),  # first 5 lines = brief intro
        "conditions": [c for c in conditions if len(c) > 10],
        "outcome": " ".join(outcome) if outcome else "Outcome not explicitly stated."
    }

def main():
    if not os.path.exists(input_path):
        print("policy_data.json not found.")
        return

    with open(input_path, "r", encoding="utf-8") as f:
        raw_data = json.load(f)

    structured = []
    for key, item in raw_data.items():
        print(f"Processing: {key}")
        blocks = extract_summary_conditions_outcome(item["content"])
        structured.append({
            "category": CATEGORY_TITLES.get(key, key),
            "summary": blocks["summary"],
            "conditions": blocks["conditions"],
            "outcome": blocks["outcome"]
        })

    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(structured, f, indent=2, ensure_ascii=False)

    print(f"✅ Structured data saved to {output_path}")

if __name__ == "__main__":
    main()
