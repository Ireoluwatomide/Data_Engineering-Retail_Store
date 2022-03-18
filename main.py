import requests
import numpy as np
import pandas as pd 
from bs4 import BeautifulSoup

class whisky_web_scraping():

    def scrape_html(self, base_url, page):
        '''
        Sending a Get request to https://www.thewhiskyexchange.com and creating a Beautiful Soup object.

        Args:
            base_url(String)
            page(Int) - The page to scrape

        Returns
            soup(Beautiful Soup Object)
        '''

        self.base_url = base_url
        self.page = page

        url = base_url + str(page)
        r = requests.get(url)
        soup = BeautifulSoup(r.content, 'lxml')

        return soup
    
    def  get_page_content(self, soup):
        '''
        Extract from soup all the html object of type div and of class product-card__content.

        Args:
            soup(BeautifulSoup Oject)

        Return:
            products_info_content(list of html objects) - List of div objects that contain the name of the beverage, the alcohol amount and percent.

        '''

        self.soup = soup

        products_info_content = soup.find_all('div', class_='product-card__content')
        return products_info_content

    def get_page_price(self, soup):
        '''
        Extract from soup all the html objevt of type div and of class product-card__data.

        Args:
            soup(BeautifulSoup Object)

        Returns:
            products_info_price(list of html objects) - List of div objects that contain the price of the beverage.
    
        '''

        self.soup = soup

        products_info_price = soup.find_all('div', class_='product-card__data')
        return products_info_price

    def get_product_name(self, products_info_content):
        '''
        Extract the name of product.

        Args:
            product_info_content(String) - The div object of class product-card__content.

        Returns:
            product_name(list) - a list of names.
        '''

        self.products_info_content = products_info_content

        product_name = []

        # Iterate through each product in the webpage
        for product in range(len(products_info_content)):

            # Extract the first class P - which holds the name of the beverage
            name_p = products_info_content[product].find_all('p')[0]

            # Extract the contents of the first paragraph - the name of the beverage
            alcohol_name = name_p.contents[0].strip()

            # Append each name to the list
            product_name.append(alcohol_name)
