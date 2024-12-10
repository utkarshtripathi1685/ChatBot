import requests
from bs4 import BeautifulSoup
import json

class WebScraper:
    def __init__(self):
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        }

    def scrape_wikipedia(self, topic):
        try:
            url = f"https://en.wikipedia.org/wiki/{topic.replace(' ', '_')}"
            response = requests.get(url, headers=self.headers)
            soup = BeautifulSoup(response.text, 'html.parser')
            
            # Get first paragraph
            first_para = soup.find('div', class_='mw-parser-output').find('p', class_=False)
            return first_para.text if first_para else "No information found."
            
        except Exception as e:
            print(f"Error scraping Wikipedia: {str(e)}")
            return None

    def get_latest_news(self, topic):
        # Implement news scraping logic
        pass 