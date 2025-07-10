import requests
from bs4 import BeautifulSoup
import json

# Define the pages to extract from
policy_pages = {
    "wellbeing": "https://www.nottingham.ac.uk/studentservices/wellbeing/student-wellbeing.aspx",
    "extenuating_circumstances": "https://www.nottingham.ac.uk/studentservices/servicedetails/extenuating-circumstances/extenuating-circumstances.aspx",
    "support_plans": "https://www.nottingham.ac.uk/studentservices/servicedetails/disability-support-services/disability-support-services.aspx"
}

def clean_text(soup):
    for tag in soup(["script", "style", "nav", "footer", "header", "form"]):
        tag.decompose()
    text = soup.get_text(separator="\n")
    lines = [line.strip() for line in text.splitlines() if line.strip()]
    return "\n".join(lines)

def fetch_and_extract(url):
    try:
        response = requests.get(url, timeout=10)
        soup = BeautifulSoup(response.text, "html.parser")
        return clean_text(soup)
    except Exception as e:
        print(f"Error fetching {url}: {e}")
        return ""

def main():
    extracted_data = {}

    for key, url in policy_pages.items():
        print(f"Extracting: {key}")
        extracted_data[key] = {
            "url": url,
            "content": fetch_and_extract(url)
        }

    # Save to JSON file
    with open("data/policy_data.json", "w", encoding="utf-8") as f:
        json.dump(extracted_data, f, indent=2, ensure_ascii=False)

    print("✅ Extraction complete. Data saved to data/policy_data.json")

if __name__ == "__main__":
    main()
