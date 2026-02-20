import scrapy


class A4icuSpiderSpider(scrapy.Spider):
    name = '4icu_spider'
    start_urls = ['https://www.4icu.org/us/universities/']
    headers = {
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,'
                  'application/signed-exchange;v=b3;q=0.9',
        'Accept-Language': 'en-GB,en-US;q=0.9,en;q=0.8',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
                      'Chrome/106.0.0.0 Safari/537.36',
        'sec-ch-ua': '"Chromium";v="106", "Google Chrome";v="106", "Not;A=Brand";v="99"',
    }
    custom_settings = {
        'FEED_URI': 'icu_universities.csv',
        'FEED_FORMAT': 'csv',
        'FEED_EXPORT_ENCODING': 'utf-8-sig',
    }

    def parse(self, response):
        for data in response.css('tr td a'):
            state_url = data.css('::attr(href)').get()
            item = dict()
            item['State'] = data.css('::text').get()
            yield response.follow(url=state_url, callback=self.parse_detail, headers=self.headers, meta={'item': item})

    def parse_detail(self, response):
        item = response.meta['item']
        for data in response.xpath('//table[contains(@class,"table-hover")]//tr[not(@class)]/following::tr[not(@class)]'):
            item['University'] = data.css('td:nth-child(2) a::text').get()
            item['Town'] = data.css('td:nth-child(3)::text').get()
            yield item

