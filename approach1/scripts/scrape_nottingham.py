import requests
from bs4 import BeautifulSoup
import json
import os

# Create output folder if it doesn't exist
os.makedirs("data/raw_web", exist_ok=True)

# List of target URLs
urls = [
    "https://student-enquiries.nottingham.ac.uk/faqs/article/FAQs-2421/en-us",
    "https://www.nottingham.ac.uk/qualitymanual/assessment-awards-and-deg-classification/pol-circs-affecting-students-study-assessments.aspx",
    "https://www.nottingham.ac.uk/qualitymanual/assessment-awards-and-deg-classification/ext-circumstances.aspx",
    "https://www.nottingham.ac.uk/studentservices/wellbeing/student-wellbeing.aspx"
]

data = []

for url in urls:
    print(f"Scraping: {url}")
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')

    content_blocks = soup.find_all(['h1', 'h2', 'h3', 'p', 'li'])

    page_data = {
        "url": url,
        "content": []
    }

    for block in content_blocks:
        text = block.get_text(strip=True)
        if text:
            page_data["content"].append(text)

    data.append(page_data)

# Save to JSON
with open("data/raw_web/nottingham_web_content.json", "w", encoding="utf-8") as f:
    json.dump(data, f, indent=2, ensure_ascii=False)

print("Web scraping complete. Data saved to 'data/raw_web/nottingham_web_content.json'")
