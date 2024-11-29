import requests
from bs4 import BeautifulSoup
import time
import random
import django
from django.core.exceptions import ObjectDoesNotExist
import os

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'goedkoperklussen.settings')
django.setup()

from product.models import Product
from activity.models import Activity


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

    @staticmethod
    def upsert_product(product_name, store_name, price, url):
        try:
            # Use url as an unique identifier.
            product = Product.objects.get(product_url=url)
            product.product_name = product_name
            product.store_name = store_name
            product.price = price

            product.save()
            print(f"Product {product_name} updated. url: {url}")

        except ObjectDoesNotExist:
            new_product = Product(
                product_name=product_name,
                store_name=store_name,
                price=price,
                product_url=url
            )

            new_product.save()
            print(f"New product {product_name} created. url: {url}")

    @staticmethod
    def create_activity(activity_name, activity_description):
        new_activity = Activity(
            activity_name=activity_name,
            activity_description=activity_description,
        )
        
        new_activity.save()
        print(f"{activity_name} created.")


class ScraperPraxis(BaseScraper):
    def scrape(self):
        result = []
        for url in self.urls:
            html = self.fetch_page(url)
            if not html:
                continue
            
            soup = BeautifulSoup(html, 'html.parser')

            # Extract product name
            product_name = soup.title.get_text(strip=True) if soup.title else "Product name not found"
            store_name = "Praxis"

            # Extract price
            price_container = soup.find('ins', class_='pdfi-fm4lyl')
            if price_container:
                main_price = price_container.find('p', class_='chakra-text pdfi-dpoqzr').get_text(strip=True)
                decimal_price = price_container.find('sup', class_='chakra-text pdfi-x924dm').get_text(strip=True)
                full_price = f"{main_price}{decimal_price}".replace(",", ".")
            else:
                full_price = False

            # Check if there's a price. If not, create an activity
            if not full_price:
                activity_name = "Price not found"
                activity_description = "Price not found. Check what might be the reason."
                self.create_activity(
                    activity_name=activity_name,
                    activity_description=activity_description
                )

            else:
                self.upsert_product(
                    product_name=product_name,
                    store_name=store_name,
                    price=full_price,
                    url=url
                )

            # Sleep for a random amount of minutes between 1 and 5 to mimic user behaviour
            time.sleep(random.randint(1, 5))


class ScraperGamma(BaseScraper):
    def scrape(self):
        result = []
        for url in self.urls:
            html = self.fetch_page(url)
            if not html:
                continue
            
            soup = BeautifulSoup(html, 'html.parser')

            # Extract product name
            title_div = soup.find('div', class_='pageheader js-pageheader-mobile')
            product_name = title_div.find('h1', itemprop='name').get_text(strip=True) if title_div else "Title not found"
            store_name = "Gamma"

            # Extract price
            price_div = soup.find('div', class_='product-price')
            if price_div:
                main_price = price_div.find('div', class_='product-price-current').get_text(strip=True)
                decimal_price = price_div.find('span', class_='product-price-decimal').get_text(strip=True)
                full_price = f"{main_price}{decimal_price}"
            else:
                full_price = False

            # Check if there's a price. If not, create an activity
            if not full_price:
                activity_name = "Price not found"
                activity_description = "Price not found. Check what might be the reason."
                self.create_activity(
                    activity_name=activity_name,
                    activity_description=activity_description
                )

            else:
                self.upsert_product(
                    product_name=product_name,
                    store_name=store_name,
                    price=full_price,
                    url=url
                )

            # Sleep for a random amount of minutes between 1 and 5 to mimic user behaviour
            time.sleep(random.randint(1, 5))


class ScraperKarwei(BaseScraper):
    def scrape(self):
        result = []
        for url in self.urls:
            html = self.fetch_page(url)
            if not html:
                continue
            
            soup = BeautifulSoup(html, 'html.parser')

            # Extract product name
            title_div = soup.find('div', class_='pageheader js-pageheader-mobile')
            product_name = title_div.find('h1', itemprop='name').get_text(strip=True) if title_div else "Title not found"
            store_name = "Karwei"

            # Extract price
            price_div = soup.find('div', class_='product-price')
            if price_div:
                main_price = price_div.find('div', class_='product-price-current').get_text(strip=True)
                decimal_price = price_div.find('span', class_='product-price-decimal').get_text(strip=True)
                full_price = f"{main_price}{decimal_price}"
            else:
                full_price = False

            # Check if there's a price. If not, create an activity
            if not full_price:
                activity_name = "Price not found"
                activity_description = "Price not found. Check what might be the reason."
                self.create_activity(
                    activity_name=activity_name,
                    activity_description=activity_description
                )

            else:
                self.upsert_product(
                    product_name=product_name,
                    store_name=store_name,
                    price=full_price,
                    url=url
                )

            # Sleep for a random amount of minutes between 1 and 5 to mimic user behaviour
            time.sleep(random.randint(1, 5))


# Example usage
"""
sm_url = "https://www.praxis.nl//praxisproductpagessitemapindex1.xml"

extractor = SitemapExtractor(sm_url)
extractor.extract_urls()
praxis_urls = extractor.get_urls()

praxis_urls = ["https://www.gamma.nl/assortiment/vouwgordijn-sten-4934-light-grey/p/C23518743"]

praxis_scraper = ScraperGamma(praxis_urls)
praxis_scraper.scrape()
"""




