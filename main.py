import openpyxl
import requests
from bs4 import BeautifulSoup
import json

def scrape_website(url):
    
    try:
        response = requests.get(url)
        response.raise_for_status()  
        soup = BeautifulSoup(response.content, 'html.parser')

        title = soup.title.text.strip() if soup.title else None
        paragraphs = [p.text.strip() for p in soup.find_all('p')]
        images = [img['src'] for img in soup.find_all('img', src=True)]
        links = [link['href'] for link in soup.find_all('a', href=True)]

        return {'url': url, 'title': title, 'paragraphs': paragraphs, 'images': images, 'links': links}
    except requests.exceptions.HTTPError as e:
        print(f"HTTP error occurred while scraping {url}: {e}")
    except Exception as e:
        print(f"Error occurred while scraping {url}: {e}")
    return None

def main():
    file_path = r'C:\Users\ACER\Desktop\Web Scraper bs4\Scrapping Python Assigment- Flair Insights.xlsx'
    wb = openpyxl.load_workbook(file_path)
    sheet = wb.active

    data = []

    for row in sheet.iter_rows(values_only=True):
        for cell in row:
            if isinstance(cell, str) and cell.startswith("http"):
                website_url = cell
                website_data = scrape_website(website_url)
                if website_data:
                    data.append(website_data)
                break  
    with open('scraped_data.json', 'w') as json_file:
        json.dump(data, json_file, indent=4)

    print("Scraping completed. Data saved to scraped_data.json")

if __name__ == "__main__":
    main()
