from datetime import datetime

import scrapy


class UsstampsScrapperSpider(scrapy.Spider):
    name = 'usstamps_scrapper'
    start_urls = ['https://www.usstampsonline.com/Product-List']
    review_request = 'https://www.usstampsonline.com/index.php?route=product/product/review&product_id={}&page={}'
    custom_settings = {
        'FEED_URI': 'review_data.csv',
        'FEED_FORMAT': 'csv',
        'FEED_EXPORT_ENCODING': 'utf-8-sig',
    }
    headers = {
        'authority': 'www.usstampsonline.com',
        'accept': 'text/html, */*; q=0.01',
        'accept-language': 'en-US,en;q=0.9',
        'sec-ch-ua': '"Google Chrome";v="105", "Not)A;Brand";v="8", "Chromium";v="105"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"Windows"',
        'sec-fetch-dest': 'empty',
        'sec-fetch-mode': 'cors',
        'sec-fetch-site': 'same-origin',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
                      'Chrome/105.0.0.0 Safari/537.36',
        'x-requested-with': 'XMLHttpRequest'
    }

    def parse(self, response):
        for data in response.css('div.product-grid .name a'):
            url = data.css('::attr(href)').get()
            yield scrapy.Request(url=url, callback=self.product_data, headers=self.headers)

        next_page = response.css('a.next::attr(href)').get()
        if next_page:
            yield scrapy.Request(url=next_page, callback=self.parse, headers=self.headers)

    def product_data(self, response):
        item = dict()
        item['model'] = response.css('li.product-model span::text').get()
        item['product_name'] = response.css('div.product-details div.page-title::text').get()
        product_id = response.css('div.stepper input[id="product-id"]::attr(value)').get()
        yield scrapy.Request(url=self.review_request.format(product_id, '1'), meta={'item': item},
                             callback=self.review_data, headers=self.headers)

    def review_data(self, response):
        pre_item = response.meta['item']
        item = pre_item
        for data in response.css('table.table-bordered'):
            item['author'] = data.css('td[style="width: 50%;"] strong::text').get()
            item['text'] = data.css('td[colspan="2"] p::text').get(' ').strip()
            review = ','.join(star.css('i.fa-star').get() for star in data.css('div.rating-stars span') if star.css('i.fa-star').get())
            item['rating'] = len(review.split(','))
            item['date_added'] = data.css("td.text-right::text").get()
            yield item

        next_page = response.css('a.next::attr(href)').get()
        if next_page:
            yield scrapy.Request(url=next_page, meta={'item': pre_item},
                                 callback=self.review_data, headers=self.headers)
