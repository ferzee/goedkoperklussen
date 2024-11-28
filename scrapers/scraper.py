import requests
from bs4 import BeautifulSoup
import time
import random


class BaseScraper:
    """
    A base scraper class for common functionality.
    """
    def __init__(self, urls):
        self.urls = urls
        self.headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.6778.86 Safari/537.36"
        }

    def fetch_page(self, url):
        """
        Fetches the HTML content of a page.
        """
        try:
            response = requests.get(url, headers=self.headers)
            response.raise_for_status()
            return response.text
        except requests.exceptions.RequestException as e:
            print(f"Error fetching {url}: {e}")
            return None

    def parse_price(self, main_price, decimal_price):
        """
        Combines main and decimal price parts into a full price.
        """
        try:
            return float(f"{main_price.replace(',', '.')}.{decimal_price}")
        except ValueError:
            print("Error parsing price.")
            return None

    def scrape(self):
        """
        Method to scrape the URLs. To be implemented by subclasses.
        """
        raise NotImplementedError("Subclasses must implement the `scrape` method.")


class ScraperPraxis(BaseScraper):
    def scrape(self):
        for url in self.urls:
            html = self.fetch_page(url)
            if not html:
                continue
            
            soup = BeautifulSoup(html, 'html.parser')

            # Extract product name
            product_name = soup.title.get_text(strip=True) if soup.title else "Product name not found"

            # Extract price
            price_container = soup.find('ins', class_='pdfi-fm4lyl')
            if price_container:
                main_price = price_container.find('p', class_='chakra-text pdfi-dpoqzr').get_text(strip=True)
                decimal_price = price_container.find('sup', class_='chakra-text pdfi-x924dm').get_text(strip=True)
                full_price = self.parse_price(main_price, decimal_price)
            else:
                full_price = "Price not found"

            print(f"{product_name}, {full_price}, {url}")
            time.sleep(random.randint(1, 5))


class ScraperGamma(BaseScraper):
    def scrape(self):
        for url in self.urls:
            html = self.fetch_page(url)
            if not html:
                continue
            
            soup = BeautifulSoup(html, 'html.parser')

            # Extract product name
            product_name_element = soup.find('div', class_='pageheader js-pageheader-mobile')
            product_name = product_name_element.find('h1', itemprop='name').get_text(strip=True) if product_name_element else "Product name not found"

            # Extract price
            price_div = soup.find('div', class_='product-price')
            if price_div:
                main_price = price_div.find('div', class_='product-price-current').get_text(strip=True)
                decimal_price = price_div.find('span', class_='product-price-decimal').get_text(strip=True)
                full_price = self.parse_price(main_price, decimal_price)
            else:
                full_price = "Price not found"

            print(f"{product_name}, {full_price}, {url}")
            time.sleep(random.randint(1, 5))


class ScraperKarwei(BaseScraper):
    def scrape(self):
        for url in self.urls:
            html = self.fetch_page(url)
            if not html:
                continue
            
            soup = BeautifulSoup(html, 'html.parser')

            # Extract product name
            product_name = soup.title.get_text(strip=True) if soup.title else "Product name not found"

            # Extract price
            price_div = soup.find('div', class_='product-price')
            if price_div:
                main_price = price_div.find('div', class_='product-price-current').get_text(strip=True)
                decimal_price = price_div.find('span', class_='product-price-decimal').get_text(strip=True)
                full_price = self.parse_price(main_price, decimal_price)
            else:
                full_price = "Price not found"

            print(f"{product_name}, {full_price}, {url}")
            time.sleep(random.randint(1, 5))


class SitemapExtractor:
    def __init__(self, sitemap_url):
        """
        Initializes the SitemapExtractor and fetches URLs from the sitemap.
        """
        self.sitemap_url = sitemap_url
        self.urls = []

    def fetch_sitemap(self):
        """
        Fetches the sitemap content and returns the parsed BeautifulSoup object.
        """
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.6778.86 Safari/537.36"
        }

        try:
            response = requests.get(self.sitemap_url, headers=headers)
            response.raise_for_status()  # Raises an HTTPError for bad responses (4xx or 5xx)
            return BeautifulSoup(response.content, 'xml')
        except requests.exceptions.RequestException as e:
            print(f"Error fetching the sitemap: {e}")
            return None

    def extract_urls(self):
        """
        Extracts URLs from the sitemap and stores them in the `urls` attribute.
        """
        soup = self.fetch_sitemap()
        if soup:
            loc_elements = soup.find_all('loc')
            self.urls = [loc.get_text(strip=True) for loc in loc_elements]
        else:
            print("Failed to parse the sitemap.")

    def get_urls(self):
        """
        Returns the list of extracted URLs.
        """
        return self.urls




# Example usage
"""
sm_url = "https://www.praxis.nl//praxisproductpagessitemapindex1.xml"

extractor = SitemapExtractor(sm_url)
extractor.extract_urls()
praxis_urls = extractor.get_urls()

praxis_scraper = ScraperPraxis(praxis_urls)
praxis_scraper.scrape()
"""
