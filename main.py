import openpyxl
import requests
from bs4 import BeautifulSoup
import json
import os

def scrape_website(url):
    try:
        response = requests.get(url)
        response.raise_for_status()
        soup = BeautifulSoup(response.content, 'html.parser')

        title = soup.title.text.strip() if soup.title else None

        paragraphs = [p.text.strip() for p in soup.find_all('p')]

        images = [img['src'] for img in soup.find_all('img', src=True)]

        links = [link['href'] for link in soup.find_all('a', href=True)]

        headers = {f'h{level}': [h.text.strip() for h in soup.find_all(f'h{level}')] for level in range(1, 7)}

        return {
            'url': url,
            'title': title,
            'paragraphs': paragraphs,
            'images': images,
            'links': links,
            'headers': headers
        }
    except requests.exceptions.HTTPError as e:
        print(f"HTTP error occurred while scraping {url}: {e}")
    except Exception as e:
        print(f"Error occurred while scraping {url}: {e}")
    return None

def main():
    file_path = r'C:\Users\ACER\Desktop\Web Scraper bs4\Scrapping Python Assigment- Flair Insights.xlsx'
    
    if not os.path.exists(file_path):
        print(f"File not found: {file_path}")
        return

    wb = openpyxl.load_workbook(file_path)
    sheet = wb.active

    data = []

    for row in sheet.iter_rows(values_only=True):
        for cell in row:
            if isinstance(cell, str) and cell.startswith("http"):
                website_url = cell
                print(f"Scraping {website_url}...")
                website_data = scrape_website(website_url)
                if website_data:
                    data.append(website_data)
                break  

    output_file = 'scraped_data.json'
    with open(output_file, 'w') as json_file:
        json.dump(data, json_file, indent=4)

    print(f"Scraping completed. Data saved to {output_file}")

if __name__ == "__main__":
    main()
