import scrapy


class ScrapyCategorySpiderSpider(scrapy.Spider):
    name = 'scrapy_category_spider'
    # allowed_domains = ['ah.nl']
    start_urls = ['https://www.ah.nl/producten']
    base_url = 'https://www.ah.nl{}'
    zyte_key = '025859a924e849f8a528b81142aaae88'
    custom_settings = {
        'CRAWLERA_ENABLED': True,
        'CRAWLERA_APIKEY': zyte_key,
        'DOWNLOADER_MIDDLEWARES': {
            'scrapy_crawlera.CrawleraMiddleware': 610
        },
        'FEED_URI': 'ah_categories.csv',
        'FEED_FORMAT': 'csv',
        'FEED_EXPORT_ENCODING': 'utf-8',
        'HTTPERROR_ALLOW_ALL': True,
    }
    headers = {
        'authority': 'www.ah.nl',
        'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,'
                  'application/signed-exchange;v=b3;q=0.9',
        'sec-ch-ua': '"Chromium";v="104", " Not A;Brand";v="99", "Google Chrome";v="104"',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
                      'Chrome/104.0.0.0 Safari/537.36 ',

    }

    def parse(self, response):
        for data in response.css("div.product-category-overview_category__1H99m"):
            cate_url = data.xpath(".//div[@class='taxonomy-card_title__JMJ3-']/a/@href").get()
            if not cate_url.startswith(self.base_url):
                cate_url = self.base_url.format(cate_url)
            yield {
                'Category_Name': data.xpath(".//div[@class='taxonomy-card_title__JMJ3-']/a/text()").get(),
                'Category_Url': cate_url,
            }


