
from kraken_scraper.scraper_main import Scraper_main


class Kraken_scraper:

    def __init__(self, url, html):

        self.url = url
        self.html = html

    def get(self):

        sm = Scraper_main(self.url, self.html)

        return sm.record
