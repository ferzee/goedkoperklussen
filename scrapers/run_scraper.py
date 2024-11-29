import django
import os
import sitemap_extractor
import scrapers
from requests.exceptions import RequestException

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'goedkoperklussen.settings')
django.setup()

from sitemap.models import Sitemap
from product.models import Product


class RunScraper:
    def __init__(self):
        # Get all sitemaps in the db
        all_active_sitemaps = Sitemap.objects.filter(is_active=True)

        for sitemap in all_active_sitemaps:
            try:
                extractor = sitemap_extractor.SitemapExtractor(sitemap_url=sitemap.sitemap_url)
                extractor.extract_urls()
                urls = extractor.get_urls()
                if not urls:
                    print(f"No urls found in sitemap {sitemap.sitemap_url}")
                    continue

                self.start_scraper(sitemap.store_name, urls)

            except RequestException as e:
                print(f"Network issue with URL {sitemap.sitemap_url}: {e}")

            except ValueError as e:
                print(f"Invalid sitemap URL {sitemap.sitemap_url}: {e}")

            except Exception as e:
                print(f"Unexpected error processing {sitemap.sitemap_url}: {e}")

    @staticmethod
    def start_scraper(store_name, urls):
        if store_name == "Praxis":
            scraper = scrapers.ScraperPraxis(urls)
            scraper.scrape()
            print(f"Completed scraping {store_name} with {len(urls)} urls")

        elif store_name == "Karwei":
            scraper = scrapers.ScraperKarwei(urls)
            scraper.scrape()
            print(f"Completed scraping {store_name} with {len(urls)} urls")

        elif store_name == "Praxis":
            scraper = scrapers.ScraperGamma(urls)
            scraper.scrape()
            print(f"Completed scraping {store_name} with {len(urls)} urls")


RunScraper()
