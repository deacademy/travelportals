import scrapy
from w3lib.html import remove_tags
from urllib.parse import urlencode
from travelportals.items import TripAdvisorHotelItem
import logging, re
import os

## Set default values in environment variable
os.environ.setdefault('API_KEY', 'sjsddddsd-ab58-4fdc-8664-shachvgvcg')
os.environ.setdefault('S3_BUCKET', 'scrapy-datalake')
os.environ.setdefault('S3_PREFIX_PATH', 'TripAdvisorHotels/')
os.environ.setdefault('SCRAPE_PAGE_LIMIT', '1')
os.environ.setdefault('SCRAPE_HOTEL_LIMIT', '1')

API_KEY = os.environ.get('API_KEY')

def get_proxy_url(url):
    # logging.info(f'Scrape url:: {url}')
    payload = {'api_key': API_KEY, 'url': url}
    proxy_url = 'https://proxy.scrapeops.io/v1/?'+urlencode(payload)
    return proxy_url

class TripadvisorSpider(scrapy.Spider):
    # handle_httpstatus_list = [403, 404]
    name = "TripAdvisor"
    allowed_domains = ["www.tripadvisor.com", "proxy.scrapeops.io"]
    scrape_urls =  [
            'https://www.tripadvisor.in/Hotels-g60713-San_Francisco_California-Hotels.html'
        ]
    retry_if_content_empty = 1
    total_page_scraped = 1
    scrape_page_limit = int(os.environ.get('SCRAPE_PAGE_LIMIT')) if os.environ.get('SCRAPE_PAGE_LIMIT') else 0
    scrape_hotel_each_page = int(os.environ.get('SCRAPE_HOTEL_LIMIT')) if os.environ.get('SCRAPE_HOTEL_LIMIT') else 0
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)  # python3.11
        logging.info(f'Allowed domain list:: {self.allowed_domains}')
        logging.info(f'Retry count if content empty:: {self.retry_if_content_empty}')
        logging.info(f'Total scrape page limit:: {self.scrape_page_limit}')
        logging.info(f'Total hotel scrape in each page:: {self.scrape_hotel_each_page}')

    def start_requests(self):

        for scrape_url in self.scrape_urls:
            return [
                scrapy.Request(
                    get_proxy_url(scrape_url),
                    callback=self.parse,
                    dont_filter = True,
                    meta={'scrape_url':scrape_url}
                )
            ]

    def extract_hotel_information(self, response):
            logging.info(f'Scraped the hotel information page status :: {response.status}')
            logging.info(f"Hotel detail page url:: {response.request.meta.get('scrape_url')}")
            
            hotel_item = TripAdvisorHotelItem()
            hotel_item['HOTEL_NAME'] = response.xpath("//h1[@id='HEADING']/text()").extract_first()
            hotel_item['RATING'] = response.xpath("//span[contains(@class,'uwJeR P')]/text()").extract_first()
            hotel_item['REVIEW_LEVEL'] = response.xpath("//div[contains(@class,'kkz')]/text()").extract_first()
            hotel_item['REVIEW_COUNT'] =  response.xpath("//span[contains(@class,'hkxYU')]/text()").extract_first()
            hotel_item['AMENTINIES'] = '\n'.join(response.xpath("//div[text()[contains(.,'Property amenities')]]/following-sibling::div[1]/div/text()").extract())
            hotel_item['FEATURES'] = '\n'.join(response.xpath("//div[text()[contains(.,'features')]]/following-sibling::div[1]/div/text()").extract())
            hotel_item['HOTEL_LISTING_PAGE_URL'] = response.request.meta.get('main_scrape_url')
            hotel_item['HOTEL_PAGE_URL'] = response.request.meta.get('scrape_url')
            hotel_item['HOTEL_LOCATION'] = response.xpath("//span[@class='fHvkI PTrfg']/text()").extract_first()
            hotel_item['CONTACT_NUMBER'] = response.xpath("//div/div/a[contains(@href, 'tel')]/span/following-sibling::span[1]/text()").extract_first()
            hotel_item['NEARLY_LANDMARK_POINTS'] = re.sub(' +', ' ', remove_tags('\n'.join(response.xpath("//div[@class='LxnRD u MC']/following-sibling::node()").extract())))
            yield hotel_item
    
    def parse(self, response):
        if response.status == 200:
            logging.info(f'Scraped the hotel list page status :: {response.status}')
            logging.info(f"Hotel list page url:: {response.request.meta.get('scrape_url')}")
            hotel_list_elements = response.xpath("//div[contains(@class, 'prw_meta_hsx_responsive_listing')]")

            ## Retry one time in case unable to find any hotel in hotet listing page
            if not len(hotel_list_elements) and self.retry_if_content_empty == 1:
                 logging.info('Retrying to fetch the same url again as hotel details unable to scrape')
                 self.retry_if_content_empty = 0
                 yield scrapy.Request(url=get_proxy_url(response.request.meta.get('scrape_url')), callback=self.parse, meta={'scrape_url':response.request.meta.get('scrape_url')})
            self.retry_if_content_empty = 1
            hotel_list_elements = response.xpath("//div[contains(@class, 'prw_meta_hsx_responsive_listing')]")
            logging.info(f'Total hotels count :: {len(hotel_list_elements)}')
            
            ## Scrape each hotel detailed information
            for hotel_detail in hotel_list_elements[: int(self.scrape_hotel_each_page) if self.scrape_hotel_each_page else len(hotel_list_elements)]:
                hotel_detail_page_url = hotel_detail.xpath(".//a[starts-with(@href,'/Hotel_Review') and @data-clicksource='HotelName']/@href").extract_first()
                single_hotel_page_link = f'https://www.tripadvisor.in{hotel_detail_page_url}'
                yield scrapy.Request(url=get_proxy_url(single_hotel_page_link), callback=self.extract_hotel_information, meta={'scrape_url': single_hotel_page_link, 'main_scrape_url': response.request.meta.get('scrape_url')})
           
            ## Scrape if next page available
            next_page_url = response.xpath("//a[text()[contains(.,'Next')]]/@href").extract_first()
            logging.info(f'Next page url:: {next_page_url}')
            
            ##Scrape only first one page by defualt
            if next_page_url and self.total_page_scraped < self.scrape_page_limit:
                self.total_page_scraped += 1
                absolute_url = f'https://www.tripadvisor.in{next_page_url}'
                yield scrapy.Request(url=get_proxy_url(absolute_url), callback=self.parse, meta={'scrape_url':absolute_url})
