import requests
import json
from bs4 import BeautifulSoup
import time
import random
import re

class BaseScraper:
    """
    A base scraper class for common functionality.
    """
    def __init__(self, urls):
        self.urls = urls
        self.headers = {
            "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36",
            "Accept": "*/*",
            "Cookie": ""
        }

    def fetch_page(self, url):
        """
        Fetches the HTML content of a page.
        """

        print(f'Scraping {url}')

        try:
            response = requests.get(url, headers=self.headers)
            response.raise_for_status()
            return response.text
        except requests.exceptions.RequestException as e:
            print(f"Error fetching {url}: {e}")
            return None

    def scrape(self):
        """
        Method to scrape the URLs. To be implemented by subclasses.
        """
        raise NotImplementedError("Subclasses must implement the `scrape` method.")


class ScraperPraxis(BaseScraper):
    def __init__(self, urls, api_url, api_key, batch_size=5):
        super().__init__(urls=urls)
        self.batch_size = batch_size
        self.api_url = api_url
        self.products = []
        self.api_key = api_key

    def scrape(self):
        """
        Scrapes each URL and collects product data.
        """
        for url in self.urls:
            html = self.fetch_page(url)

            if not html:
                continue
            
            soup = BeautifulSoup(html, 'html.parser')

            product_name = soup.title.get_text(strip=True) if soup.title else "Product name not found"

            product_description_div = soup.find('div', class_='mxd-description-container').find('div')
            product_description = product_description_div.get_text(strip=True) if product_description_div else ""

            ean_div = soup.find('ul', class_='eans-list').find_all('li')
            ean_code = [ean_code.get_text(strip=True) for ean_code in ean_div][0] if ean_div else ""

            store_name = "Praxis"

            img_url = soup.find('picture').find('img')
            img_url = img_url['src']

            price_container = soup.find('ins', class_='pdfi-1e34aan')
            if price_container:
                main_price = price_container.find('p', class_='chakra-text pdfi-dpoqzr').get_text(strip=True)
                decimal_price = price_container.find('sup', class_='chakra-text pdfi-x924dm').get_text(strip=True)
                full_price = float(f"{main_price}{decimal_price}".replace(",", "."))
            else:
                full_price = 0.0

            product_data = {
                "product_name": product_name,
                "product_description": product_description,
                "ean_code": ean_code,
                "store_name": store_name,
                "current_price": full_price,
                "product_url": url,
                "img_url": img_url
            }
            self.products.append(product_data)

            print(f'Succesfully scraped {url}')

            if len(self.products) >= self.batch_size:
                self.send_data_in_batches(self.products)
                self.products = []

            time.sleep(1)

        # Send any remaining products that didn't fill up a full batch
        if self.products:
            self.send_data_in_batches(self.products)

    def send_data_in_batches(self, products):
        """
        Sends the products in batches to the Django API.
        """
        payload = {'products': products}
        headers = {
            'Content-Type': 'application/json',
            'X-API-Key': self.api_key
        }

        # Send the batch to the API
        try:
            response = requests.post(self.api_url, data=json.dumps(payload), headers=headers)

            if response.status_code == 200:
                print(f"Batch sent successfully. Number of products: {len(products)}")
            else:
                print(f"Error sending batch. Status Code: {response.status_code}, Response: {response.text}")
        except requests.exceptions.RequestException as e:
            print(f"Error sending batch: {e}")


class ScraperGamma(BaseScraper):
    def __init__(self, urls, api_url, api_key, batch_size=5):
        super().__init__(urls=urls)
        self.batch_size = batch_size  # Define the batch size
        self.api_url = api_url  # Your Django API endpoint URL
        self.api_key = api_key  # Store the API key for sending data
        self.products = []  # List to store all scraped products

    def scrape(self):
        """
        Scrapes the URLs and collects product data.
        """
        for url in self.urls:
            html = self.fetch_page(url)
            if not html:
                continue

            soup = BeautifulSoup(html, 'html.parser')

            title_div = soup.find('div', class_='pageheader js-pageheader-mobile')
            product_name = title_div.find('h1', itemprop='name').get_text(
                strip=True) if title_div else "Title not found"

            description_div = soup.find('div', itemprop='description')
            product_description = description_div.text.strip() if description_div else ""

            ean_row = soup.find('th', string=re.compile(r'^\s*EAN\s*$', re.IGNORECASE))
            ean_code = ean_row.find_next('td').find('span', class_='feature-value').text.strip() if ean_row else ""

            store_name = "Gamma"

            meta_tag = soup.find('meta', {'itemprop': 'image'})
            img_url = meta_tag['content'] if meta_tag and meta_tag.has_attr('content') else None

            price_div = soup.find('div', class_='product-price')
            if price_div:
                main_price = price_div.find('div', class_='product-price-current').get_text(strip=True)
                decimal_price = price_div.find('span', class_='product-price-decimal').get_text(strip=True)
                full_price = float(f"{main_price}{decimal_price}")
            else:
                full_price = 0.0

            product_data = {
                "product_name": product_name,
                "product_description": product_description,
                "ean_code": ean_code,
                "store_name": store_name,
                "current_price": full_price,
                "product_url": url,
                "img_url": img_url
            }
            self.products.append(product_data)

            print(f'Succesfully scraped {url}')

            # If batch size is reached, send the data
            if len(self.products) >= self.batch_size:
                self.send_data_in_batches(self.products)
                self.products = []  # Reset the list after sending

            time.sleep(1)

        # Send any remaining products in the batch
        if self.products:
            self.send_data_in_batches(self.products)

    def send_data_in_batches(self, products):
        """
        Sends the products in batches to the Django API.
        """
        payload = {'products': products}  # Wrap the batch in the 'products' key
        headers = {
            'Content-Type': 'application/json',
            'X-API-Key': self.api_key  # Add the API key header here when sending the data
        }

        # Send the batch to the API
        try:
            response = requests.post(self.api_url, data=json.dumps(payload), headers=headers)

            if response.status_code == 200:
                print(f"Batch sent successfully. Number of products: {len(products)}")
            else:
                print(f"Error sending batch. Status Code: {response.status_code}, Response: {response.text}")
        except requests.exceptions.RequestException as e:
            print(f"Error sending batch: {e}")


class ScraperKarwei(BaseScraper):
    def __init__(self, urls, api_url, api_key, batch_size=5):
        super().__init__(urls=urls)
        self.batch_size = batch_size  # Define the batch size
        self.api_url = api_url  # Your Django API endpoint URL
        self.api_key = api_key  # Store the API key for sending data
        self.products = []  # List to store all scraped products

    def scrape(self):
        """
        Scrapes the URLs and collects product data.
        """
        for url in self.urls:
            html = self.fetch_page(url)
            if not html:
                continue

            soup = BeautifulSoup(html, 'html.parser')

            title_div = soup.find('div', class_='pageheader js-pageheader-mobile')
            product_name = title_div.find('h1', itemprop='name').get_text(
                strip=True) if title_div else "Title not found"

            description_div = soup.find('div', itemprop='description')
            product_description = description_div.text.strip() if description_div else ""

            ean_row = soup.find('th', string=re.compile(r'^\s*EAN\s*$', re.IGNORECASE))
            ean_code = ean_row.find_next('td').find('span', class_='feature-value').text.strip() if ean_row else ""

            store_name = "Karwei"

            meta_tag = soup.find('meta', {'itemprop': 'image'})
            img_url = meta_tag['content'] if meta_tag and meta_tag.has_attr('content') else None

            price_div = soup.find('div', class_='product-price')
            if price_div:
                main_price = price_div.find('div', class_='product-price-current').get_text(strip=True)
                decimal_price = price_div.find('span', class_='product-price-decimal').get_text(strip=True)
                full_price = float(f"{main_price}{decimal_price}")
            else:
                full_price = 0.0

            product_data = {
                "product_name": product_name,
                "product_description": product_description,
                "ean_code": ean_code,
                "store_name": store_name,
                "current_price": full_price,
                "product_url": url,
                "img_url": img_url
            }
            self.products.append(product_data)

            print(f'Succesfully scraped {url}')

            if len(self.products) >= self.batch_size:
                self.send_data_in_batches(self.products)
                self.products = []  # Reset the list after sending

            time.sleep(1)

        # Send any remaining products in the batch
        if self.products:
            self.send_data_in_batches(self.products)

    def send_data_in_batches(self, products):
        """
        Sends the products in batches to the Django API.
        """
        payload = {'products': products}  # Wrap the batch in the 'products' key
        headers = {
            'Content-Type': 'application/json',
            'X-API-Key': self.api_key  # Add the API key header here when sending the data
        }

        # Send the batch to the API
        try:
            response = requests.post(self.api_url, data=json.dumps(payload), headers=headers)

            if response.status_code == 200:
                print(f"Batch sent successfully. Number of products: {len(products)}")
            else:
                print(f"Error sending batch. Status Code: {response.status_code}, Response: {response.text}")
        except requests.exceptions.RequestException as e:
            print(f"Error sending batch: {e}")
