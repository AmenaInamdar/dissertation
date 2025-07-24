import os
import json

# Input folders
pdf_text_dir = "data/raw_pdfs/text"
web_json_file = "data/raw_web/nottingham_web_content.json"
output_file = "data/structured/nottingham_policies.json"

structured_data = []

# --- PDF .txt files ---
for filename in os.listdir(pdf_text_dir):
    if filename.endswith(".txt"):
        file_path = os.path.join(pdf_text_dir, filename)
        with open(file_path, "r", encoding="utf-8") as f:
            raw_text = f.read()

        sections = raw_text.split("\n\n")  # crude section split
        for i, section in enumerate(sections):
            if len(section.strip()) < 40:
                continue  # skip very short lines
            structured_data.append({
                "source": filename,
                "section": f"PDF Section {i+1}",
                "tags": [],
                "content": section.strip()
            })

# --- Web scraped JSON ---
with open(web_json_file, "r", encoding="utf-8") as f:
    web_pages = json.load(f)

for page in web_pages:
    url = page["url"]
    for i, block in enumerate(page["content"]):
        structured_data.append({
            "source": url,
            "section": f"Web Block {i+1}",
            "tags": [],
            "content": block
        })

# Save output
os.makedirs(os.path.dirname(output_file), exist_ok=True)
with open(output_file, "w", encoding="utf-8") as f:
    json.dump(structured_data, f, indent=2, ensure_ascii=False)

print(f"Structured data saved to {output_file}")
