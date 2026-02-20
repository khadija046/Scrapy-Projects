import json
import scrapy


class DetailSpiderSpider(scrapy.Spider):
    name = 'scrapper_details'
    start_urls = ['https://www.lowes.com/']
    zyte_key = '5871ec424f0a479ab721b3a757703580'
    custom_settings = {
        'CRAWLERA_ENABLED': True,
        'CRAWLERA_APIKEY': zyte_key,
        'DOWNLOADER_MIDDLEWARES': {
            'scrapy_crawlera.CrawleraMiddleware': 610
        },
        'FEED_URI': 'lowes_details.csv',
        'FEED_FORMAT': 'csv',
        'FEED_EXPORT_ENCODING': 'utf-8',
        'HTTPERROR_ALLOW_ALL': True,
    }

    request_api = '{}/products?offset={}&adjustedNextOffset={}&nearByStores=2512,2955,0289,1633,1631'
    price_api = 'https://www.lowes.com/pd/{}/productdetail/1985/Guest'
    base_url = 'https://www.lowes.com{}'
    headers = {
        'authority': 'www.lowes.com',
        'accept': 'application/json',
        'accept-language': 'en-US,en;q=0.9',
        'sec-ch-ua': '"Google Chrome";v="105", "Not)A;Brand";v="8", "Chromium";v="105"',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
                      'Chrome/105.0.0.0 Safari/537.36 ',
        'X-Crawlera-Region': 'us',
        'X-Crawlera-Profile': 'pass'
    }

    def parse(self, response):
        for data in response.xpath('//div[contains(@class,"jaXDpy")]/div/following::div/a[contains(@class,"bgwsNI")]'):
            cate_url = data.xpath('./@href').get()
            if not cate_url.startswith(self.base_url):
                cate_url = self.base_url.format(cate_url)
            yield scrapy.Request(url=cate_url, callback=self.category_scrap, headers=self.headers)

    def category_scrap(self, response):
        if response.css('.carousel-wrapper a').get():
            for data in response.css('.carousel-wrapper a'):
                cate_url = data.css('::attr(href)').get()
                if not cate_url.startswith(self.base_url):
                    cate_url = self.base_url.format(cate_url)
                yield scrapy.Request(url=cate_url, callback=self.sub_category, headers=self.headers)
        else:
            if response.url == 'https://www.lowes.com/c/Flooring?int_cmp=Home%3AA2%3AFlooring%3Aother%3APC_Flooring':
                for data in response.css('div[data-businessname="na"] .fhuHA-D a.bgwsNI'):
                    cate_url = data.css('::attr(href)').get()
                    if not cate_url.startswith(self.base_url):
                        cate_url = self.base_url.format(cate_url)
                    yield scrapy.Request(url=cate_url, callback=self.sub_category, headers=self.headers)
            else:
                if response.css('.iaaTdj div[data-businessname="na"] a.bgwsNI').get():
                    for data in response.css('.iaaTdj div[data-businessname="na"] a.bgwsNI'):
                        cate_url = data.css('::attr(href)').get()
                        if not cate_url.startswith(self.base_url):
                            cate_url = self.base_url.format(cate_url)
                        yield scrapy.Request(url=cate_url, callback=self.sub_category, headers=self.headers)
                else:
                    for data in response.css('div[data-businessname="na"] a.bgwsNI'):
                        cate_url = data.css('::attr(href)').get()
                        if not cate_url.startswith(self.base_url):
                            cate_url = self.base_url.format(cate_url)
                        yield scrapy.Request(url=cate_url, callback=self.sub_category, headers=self.headers)

    def sub_category(self, response):
        if response.css('.hDbgSQ').get():
            item = {'offset': 24,
                    'req_url': response.url}
            yield scrapy.Request(
                url=self.request_api.format(response.url, '0', '24'), meta={'item': item}
                , callback=self.parse_data, headers=self.headers)
        else:
            if response.css('.sm-12 .bbnBKv a.iGfemI').get():
                for data in response.css('.sm-12 .bbnBKv a.iGfemI'):
                    cate_url = data.css('::attr(href)').get()
                    if not cate_url.startswith(self.base_url):
                        cate_url = self.base_url.format(cate_url)
                    item = {'offset': 24,
                            'req_url': cate_url}
                    yield scrapy.Request(
                        url=self.request_api.format(cate_url, '0', '24'), meta={'item': item}
                        , callback=self.parse_data, headers=self.headers)
            else:
                if response.css('div[data-businessname="na"] a.bgwsNI').get():
                    for data in response.css('div[data-businessname="na"] a.bgwsNI'):
                        cate_url = data.css('::attr(href)').get()
                        if not cate_url.startswith(self.base_url):
                            cate_url = self.base_url.format(cate_url)
                        item = {'offset': 24,
                                'req_url': cate_url}
                        yield scrapy.Request(
                            url=self.request_api.format(cate_url, '0', '24'), meta={'item': item}
                            , callback=self.parse_data, headers=self.headers)
                else:
                    for data in response.css('.sc-98d7ri_engage-common-4 div[data-businessname="na"] a.bgwsNI'):
                        cate_url = data.css('::attr(href)').get()
                        if not cate_url.startswith(self.base_url):
                            cate_url = self.base_url.format(cate_url)
                        item = {'offset': 24,
                                'req_url': cate_url}
                        yield scrapy.Request(
                            url=self.request_api.format(cate_url, '0', '24'), meta={'item': item}
                            , callback=self.parse_data, headers=self.headers)

    def parse_data(self, response):
        try:
            result = json.loads(response.body)
            item = response.meta['item']
            for data in result.get('itemList', []):
                pro_sku = data.get('product', {}).get('omniItemId', '')
                item_data = {
                    'sku': data.get('product', {}).get('omniItemId', ''),
                    'description': data.get('product', {}).get('description', ''),
                    'detail_url': self.base_url.format(data.get('product', {}).get('pdURL', '')),
                }
                yield scrapy.Request(
                    url=self.price_api.format(pro_sku),
                    meta={'item': item_data}, callback=self.price_data, headers=self.headers)
            previous_offset = item.get('offset', '')
            next_offset = result.get('adjustedNextOffset', '')
            next_page = result.get('pagination', '').get('page', '') + 1
            total_pages = result.get('pagination', '').get('pageCount', '')
            if next_page <= total_pages:
                item['offset'] = next_offset
                yield scrapy.Request(url=self.request_api.format(item.get('req_url', ''), previous_offset, next_offset)
                                     , meta={'item': item}, callback=self.parse_data, headers=self.headers)
        except:
            pass

    def price_data(self, response):
        try:
            result = json.loads(response.body)
            item = response.meta['item']
            pro_id = result.get('productId', '')
            price_data = result.get('productDetails', '').get(pro_id, {}).get('price', {})
            if price_data:
                item['Price'] = price_data.get('analyticsData', {}).get('sellingPrice', '') if pro_id else ' '
                yield item
            else:
                item['Price'] = ''
                yield item
        except:
            pass
