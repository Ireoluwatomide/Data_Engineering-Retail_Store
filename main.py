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

        return product_name

    def get_product_alcohol_percent(self, products_info_content):
        '''
        Extract the alcohol percent of product.

        Args:
            products_info_content(String) - The div object of class product-card__content.

        Returns:
            product_al_percent(List) - A list of alcohol percent.
        '''

        self.products_info_content = products_info_content

        product_al_percent = []

        # Iterate  through each product in the webpage
        for product in range(len(products_info_content)):

            # Extract the second P - which holds the alcohol values
            al_p = products_info_content[product].find_all('p')[1]

            # Apply string manipulation to extract the alcohol percent
            alcohol_percent_str = al_p.contents[0].strip()
            start_location_percent = alcohol_percent_str.find('/')
            end_location_percent = alcohol_percent_str.find('%')
            alcohol_percent = alcohol_percent_str[start_location_percent + 2:end_location_percent]

            # Append each alcohol percent to the list
            product_al_percent.append(alcohol_percent)

        return product_al_percent

    def get_product_alcohol_amount(self, products_info_content):
        '''
        Extract the alcohol amount of product.

        Args:
            products_info_content(String) - The div object of class product_card__content.

        Returns:
            product_al_amount(List) - A list of alcohol amount.
        '''

        self.products_info_content = products_info_content

        product_al_amount = []

        # Iterate through each product in the webpage
        for product in range(len(products_info_content)):

            # Extract the second class P - which holds alcohol values
            al_p = products_info_content[product].find_all('p')[1]

            # Apply string manipulation to extract the alcohol amount
            alcohol_amount_str = al_p.contents[0].strip()
            start_location_amount = 0
            end_location_amount = alcohol_amount_str.find('cl')
            alcohol_amount = alcohol_amount_str[start_location_amount:end_location_amount]

            # Append each alcohol amount to list
            product_al_amount.append(alcohol_amount)

        return product_al_amount

    def get_product_price(self, products_info_price):
        '''
        Extract the price of product.

        Args:
            products_info_price(String) - The div object of class product-card__data.

        Returns:
            product_price(list) - A list of prices.
        '''

        self.produts_info_price = products_info_price

        product_price = []

        # Iterate through each product in the webpage
        for product in range(len(products_info_price)):

            # Extract the price of each product
            alcohol_price = products_info_price[product].contents[0].contents[0].replace('£', '').strip()
            '''
            al_p = products_info_price[product].find_all('p')[0]

            alcohol_price_str = al_p.contents[0].strip()
            start_location_price = alcohol_price_str.find('£')
            end_location_price = alcohol_price_str.find('5)
            alcohol_price = alcohol_price_str[start_location_price + 1:end_location_price + 1]
            '''

            # Append each alcohol price to the list
            product_price.append(alcohol_price)
        
        return(product_price)

    def create_df(self, names, alcohol_amount, alcohol_percent, price):
        '''
        Create a DataFrame that will hold the extracted data.

        Args:
            names(List) - A list of product names.
            alcohol_amount(List) - A list of products alcohol amounts.
            alcohol_percent(List) - A list of product alcohol percent.
            price(List) - A list of product prices.

        Returns:
            original_df(DataFrame)
        '''

        self.names = names
        self.alcohol_amount = alcohol_amount
        self.alcohol_percent = alcohol_percent
        self.price = price

        # Create a DataFrame
        original_df = pd.DataFrame(names, columns=['Product_Name'])
        original_df['Alcohol_Percent'] = alcohol_percent
        original_df['Alcohol_Amount'] = alcohol_amount
        original_df['Alcohol_Price'] = price

        return original_df