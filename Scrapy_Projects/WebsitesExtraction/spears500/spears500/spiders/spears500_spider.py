import csv
import json

import scrapy


class Spears500SpiderSpider(scrapy.Spider):
    name = 'spears500_spider'
    custom_settings = {
        'FEED_URI': 'spears500.csv',
        'FEED_FORMAT': 'csv',
        'FEED_EXPORT_ENCODING': 'utf-8-sig',
    }
    headers = {
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,'
                  'application/signed-exchange;v=b3;q=0.9',
        'Accept-Language': 'en-GB,en-US;q=0.9,en;q=0.8',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
                      'Chrome/106.0.0.0 Safari/537.36',
        'sec-ch-ua': '"Chromium";v="106", "Google Chrome";v="106", "Not;A=Brand";v="99"',
    }

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.request_site = self.get_search_urls()

    def get_search_urls(self):
        with open('Book1.csv', 'r', encoding='utf-8-sig') as reader:
            return list(csv.DictReader(reader))

    def start_requests(self):
        for site in self.request_site:
            website = site.get('website')
            yield scrapy.Request(url=website, callback=self.parse, headers=self.headers)

    def parse(self, response):
        yield {
            'Name': response.css('h1.headline::text').get('').strip(),
            'Email': response.css('p.mail a::text').get('').strip(),
            'Phone': response.css('div.contact-details-section a.remove-decorations::text').get('').strip(),
            'Detail_url': response.url
        }
