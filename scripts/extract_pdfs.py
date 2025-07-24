import pdfplumber
import os

pdf_dir = "data/raw_pdfs/"
output_dir = "data/raw_pdfs/text/"
os.makedirs(output_dir, exist_ok=True)

for file in os.listdir(pdf_dir):
    if file.endswith(".pdf"):
        text_chunks = []
        file_path = os.path.join(pdf_dir, file)

        with pdfplumber.open(file_path) as pdf:
            for page in pdf.pages:
                text = page.extract_text()
                if text:
                    text_chunks.append(text.strip())

        output_file = file.replace(".pdf", ".txt")
        with open(os.path.join(output_dir, output_file), "w", encoding="utf-8") as f:
            f.write("\n\n".join(text_chunks))

        print(f"Extracted: {output_file}")
