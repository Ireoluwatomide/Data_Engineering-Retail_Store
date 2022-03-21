# Import whisky_web_scraping class
from scraper import whisky_web_scraping

# Create a scraper object
scraper = whisky_web_scraping()

# Scrape data
data = scraper.scrape_whisky(number_of_pages = 96)