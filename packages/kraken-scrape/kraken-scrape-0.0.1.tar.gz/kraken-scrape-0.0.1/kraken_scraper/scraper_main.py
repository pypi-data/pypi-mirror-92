

from bs4 import BeautifulSoup
from kraken_scraper.scraper_schemas import Extract_schema
import requests
import urllib.parse
from urllib.parse import urlparse
import json
import pprint
pp = pprint.PrettyPrinter(indent=4)


    
class Scraper_main:

    def __init__(self, url = None, html = None):

        self.url = url

        # Initialize variables
        self.title = None
        self.text = None
        self.links = []
        self.schemas = []
        self.images = []
        self.feeds = []
        self.html = html

        # Start scraping
        self.get()


    @property 
    def record(self):
        record = {
            '@type': 'schema:webpage',
            '@id': self.url,
            'schema:name': self.url,
            'schema:title': self.title,
            'schema:content': self.text,
            'kraken:related': self._extracts

        }

        return record

    @property
    def _extracts(self):

        extracts = []
        extracts += self.schemas
        extracts += self.images
        extracts += self.feeds
        extracts += self.html


    def get(self):


        # Get html content
        if not self.html:
            self._get_html_from_site()

        # Initialize beautifulsoup
        self._get_soup()

        # Get title 
        self._extract_title()

        # Get text from webpage
        self._extract_text()

        # Get links
        self._extract_links()

        # Get images
        self._extract_images()

        # Get structured data
        self._extract_schema()
        
        # Get feeds
        self._extract_feeds()



        return


    
    def get_all(self, url):


        url_list = ['https://suburbanmen.com']

        url_done = []


        scrape_run = 0

        while len(url_list) > 0:

            url = url_list.pop(0)

            url_done.append(url)

            scrape_run +=1
            print('Scrape run', scrape_run)

            print('Scraping', url)
            print('Items in list', len(url_list))

            scrape = Scraper_main(url)

            scrape.get()

            pp.pprint(scrape.stats)

            links = scrape.links

            for i in links:
                link_url = i.get('schema:url', None)
                if link_url not in url_list and link_url not in url_done:
                    url_list.append(link_url)

            filename = url
            filename = filename.replace('/', '_')
            filepath = 'scrape/' + filename
            f = open(filepath, "w")
            f.write(json.dumps(scrape.record, default=str))
            f.close()





    def _get_html_from_site(self):

        r = requests.get(self.url)

        self.html = r.content




    def _get_soup(self):

        self.soup = BeautifulSoup(self.html, 'html.parser')



    def _extract_title(self):


        if not self.soup:
            return

        if not self.soup.title:
            return


        # Get title
        self.title = self.soup.title.string


    def _extract_text(self):

        # Get text from webpage
        self.text =  self.soup.get_text()


    def _extract_links(self):

        self.links = []

        # Get links
        links = self.soup.find_all('a')
        
        for link in links:
            link_url = link.get('href', None)
            link_title = link.text

            # Convert to absolute url
            link_url = urllib.parse.urljoin(self.url, link_url)

            # Compile into structured record
            link_record = {
                '@type': 'schema:webpage',
                'schema:title': link_title,
                'schema:url': link_url
            }

            # Add to list if url exist
            if link_record.get('schema:url', None):
                self.links.append(link_record)



    def _extract_schema(self):

        if not self.html:
            return

        extract_schema = Extract_schema(self.url, self.html)

        self.schemas = extract_schema.schemas


    def _extract_images(self):


        images = self.soup.findAll('img')

        for img in images:

            image_url = img.get('src', None)

            # Convert to absolute url
            image_url = urllib.parse.urljoin(self.url, image_url)

            # Compile into structured record
            image = {
                '@type': 'schema:image',
                'schema:title': img.get('title', None),
                'schema:contenturl': image_url
            }
            
            # Skip if already in list
            if image in self.images:
                continue


            # Add to list if url exist
            if image.get('schema:contenturl', None):
                self.images.append(image)



    def _extract_feeds(self):

        feeds = self.soup.findAll(type='application/rss+xml') + self.soup.findAll(type='application/atom+xml')

        for feed in feeds:

            feed_url = feed.get('href', None)

            # Convert to absolute url
            feed_url = urllib.parse.urljoin(self.url, feed_url)

            # Compile into structured record
            feed_record = {
                '@type': 'schema:datafeed',
                'schema:title': feed.get('title', None),
                'schema:url': feed_url
            }
            

            # Skip if already in list
            if feed_record  in self.feeds:
                continue

            # Add to list if url exist
            if feed_record.get('schema:url', None):
                self.feeds.append(feed_record)




    @property
    def related_records(self):

        self._related_records = []


        self._related_records += self.links
        self._related_records += self.schemas
        self._related_records += self.images

        return self._related_records

    @property
    def record(self):

        self._record = {

            'schema:name': self.title,
            'schema:url': self.url,
            'schema:text': self.text,
            'kraken:related': self.related_records
        }

        return self._record


    @property 
    def stats(self):

        self._stats = {
            'links': self._get_stat_links(),
            'schemas': self._get_stat_schemas(),
            'images': self._get_stat_images(),
            'feeds': self._get_stat_feeds()
        }

        return self._stats



    def _get_stat_images(self):

        record = {
            'No of images': len(self.images)
        }

        return record


    def _get_stat_feeds(self):

        record = {
            'No of feeds': len(self.feeds)
        }

        return record


    def _get_stat_links(self):


        # Count domains
        same_domain = 0
        different_domain = 0
        external_domain_list = []

        for i in self.links:
            i_url = i.get('schema:url', None)
            o = urlparse(i_url)
            link_domain = o.netloc

            link_domain = link_domain.replace('www.', '')

            u = urlparse(self.url)
            main_domain = u.netloc
            main_domain = main_domain.replace('www.', '')

            if link_domain and link_domain == main_domain:
                same_domain += 1
            else:
                different_domain += 1

                if link_domain not in external_domain_list:
                    external_domain_list.append(link_domain)

    

        record = {
            'internal links': same_domain,
            'external links': different_domain,
            'external domains': external_domain_list,
            'total links': same_domain + different_domain
        }

        return record

    def _get_stat_schemas(self):

        record_types = {}

        for i in self.schemas:
            record_type = i.get('@type', None)
            if not record_types.get(record_type, None):
                record_types[record_type] = 1
            else:
                record_types[record_type] += 1

        return record_types
