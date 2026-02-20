import csv
import json
from datetime import datetime

import scrapy


class DetailSpiderSpider(scrapy.Spider):
    name = 'detail_spider'
    request_api = 'https://www.ah.nl/zoeken/api/products/search?page={}&size={}&{}'
    base_url = 'https://www.ah.nl{}'
    zyte_key = '025859a924e849f8a528b81142aaae88'
    custom_settings = {
        'CRAWLERA_ENABLED': True,
        'CRAWLERA_APIKEY': zyte_key,
        'DOWNLOADER_MIDDLEWARES': {
            'scrapy_crawlera.CrawleraMiddleware': 610
        },
        'FEED_URI': 'alphabetical_details.csv',
        'FEED_FORMAT': 'csv',
        'FEED_EXPORT_ENCODING': 'utf-8',
        'HTTPERROR_ALLOW_ALL': True,
    }

    headers = {
        'authority': 'www.ah.nl',
        'accept': 'application/json',
        'sec-ch-ua': '"Chromium";v="104", " Not A;Brand";v="99", "Google Chrome";v="104"',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
                      'Chrome/104.0.0.0 Safari/537.36',
        'X-Crawlera-Profile': 'pass'
    }

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.request_key = self.get_search_urls()

    def get_search_urls(self):
        with open('alphabetical_categories.csv', 'r', encoding='utf-8-sig') as reader:
            return list(csv.DictReader(reader))

    def start_requests(self):
        for data in self.request_key:
            payload = {'key': data.get('Category_Url', '').split('/')[-1],
                       'page_no': 1}
            cate_slug = data.get('Category_Url', '').split('/')[-2]
            if cate_slug == 'merk':
                url = self.request_api.format('1', '10', 'brandSlug={}')
                payload['category_url'] = data.get('Category_Url', '')
                yield scrapy.Request(url=url.format(data.get('Category_Url', '').split('/')[-1]),
                                     meta={'payload': payload},
                                     callback=self.parse, headers=self.headers)
            else:
                url = self.request_api.format('1', '135', 'taxonomySlug={}')
                payload['category_url'] = data.get('Category_Url', '')
                yield scrapy.Request(url=url.format(data.get('Category_Url', '').split('/')[-1]),
                                     meta={'payload': payload},
                                     callback=self.parse, headers=self.headers)

    def parse(self, response):
        result = json.loads(response.body)
        payload = response.meta['payload']
        rank = 1
        for data in result.get('cards', []):
            pro_data = data.get('products', [])
            if pro_data[0]:
                pro_url = pro_data[0].get('link', '')
                if not pro_url.startswith(self.base_url):
                    pro_url = self.base_url.format(pro_url)
                yield {
                    'Product_id': pro_data[0].get('id', ''),
                    'Product_Name': pro_data[0].get('title', ''),
                    'Brand_Name': pro_data[0].get('brand', ''),
                    'Unit_Size': pro_data[0].get('price', {}).get('unitSize', ''),
                    'Price': pro_data[0].get('price', {}).get('now', ''),
                    'Nutri_Score': pro_data[0].get('highlight', {}).get('name', ''),
                    'Property_Icon': ', '.join(icon.get('title', '') for icon in pro_data[0].get('propertyIcons', [])),
                    'Images_url': ', '.join(image.get('url', '') for image in pro_data[0].get('images', [])),
                    'Category_Rank': pro_data[0].get('category', ''),
                    'Product_Rank': rank,
                    'Page_no': payload.get('page_no', ''),
                    'pro_url': pro_url,
                    'page_url': response.url,
                    'Category_url': payload.get('category_url', ''),
                    'TimeStamp': datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                }
            rank += 1
        total_pages = result.get('page', {}).get('totalPages', '')
        next_page = payload.get('page_no', '') + 1
        cate_slug = payload.get('category_url', '').split('/')[-2]
        if next_page <= total_pages:
            payload['page_no'] = next_page
            if cate_slug == 'merk':
                url = self.request_api.format(next_page, '10', 'brandSlug={}')
                payload['category_url'] = payload.get('category_url', '')
                yield scrapy.Request(url=url.format(payload.get('category_url', '').split('/')[-1]),
                                     meta={'payload': payload},
                                     callback=self.parse, headers=self.headers)
            else:
                url = self.request_api.format(next_page, '135', 'taxonomySlug={}')
                payload['category_url'] = payload.get('Category_Url', '')
                yield scrapy.Request(url=url.format(payload.get('category_url', '').split('/')[-1]),
                                     meta={'payload': payload},
                                     callback=self.parse, headers=self.headers)
