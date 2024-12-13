import requests
from bs4 import BeautifulSoup


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
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.6778.86 Safari/537.36",
        }

        try:
            response = requests.get(self.sitemap_url, headers=headers)
            response.raise_for_status()  # Raises an HTTPError for bad responses (4xx or 5xx)
            return BeautifulSoup(response.content, 'lxml')
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
