import sitemap_extractor
import scrapers
from requests.exceptions import RequestException
import requests

class RunScraper:

    def __init__(self, get_api_url, post_api_url):
        self.api_key = ""
        self.post_api_url = post_api_url
        self.get_api_url = get_api_url
        self.headers = {'X-API-Key': self.api_key}

        all_active_sitemaps = self.get_sitemaps()

        for sitemap in all_active_sitemaps:
            sitemap_url = sitemap['sitemap_url']
            if sitemap["is_active"]:
                try:
                    extractor = sitemap_extractor.SitemapExtractor(sitemap_url=sitemap_url)
                    extractor.extract_urls()
                    urls = extractor.get_urls()
                    if not urls:
                        print(f"No urls found in sitemap {sitemap_url}")
                        continue

                    self.start_scraper(sitemap['store_name'], urls)

                except RequestException as e:
                    print(f"Network issue with URL {sitemap_url}: {e}")

                except ValueError as e:
                    print(f"Invalid sitemap URL {sitemap_url}: {e}")

                except Exception as e:
                    print(f"Unexpected error processing {sitemap_url}: {e}")


    def get_sitemaps(self):

        try:
            response = requests.get(self.get_api_url, headers=self.headers)

            if response.status_code == 200:
                return response.json()
            else:
                print(f"Error: Unable to fetch data. Status code: {response.status_code}")
                print(f"Response: {response.text}")
                return None

        except requests.exceptions.RequestException as e:
            print(f"An error occurred: {e}")
            return None

    def start_scraper(self, store_name, urls):
        if store_name == "Praxis":
            scraper = scrapers.ScraperPraxis(urls, api_key=self.api_key, api_url=self.post_api_url)
            scraper.scrape()
            print(f"Completed scraping {store_name} with {len(urls)} urls")

        elif store_name == "Karwei":
            scraper = scrapers.ScraperKarwei(urls, api_key=self.api_key, api_url=self.post_api_url)
            scraper.scrape()
            print(f"Completed scraping {store_name} with {len(urls)} urls")

        elif store_name == "Gamma":
            scraper = scrapers.ScraperGamma(urls, api_key=self.api_key, api_url=self.post_api_url)
            scraper.scrape()
            print(f"Completed scraping {store_name} with {len(urls)} urls")


RunScraper(
    get_api_url="https://goedkoopklussen.com/sitemaps/",
    post_api_url="https://goedkoopklussen.com/api/products/create",
)

