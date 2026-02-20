import json

import scrapy


class QuestionScrapperSpider(scrapy.Spider):
    name = 'without_scrapper'
    request_api = 'https://search.realself.com/questions-api?offset={}&limit=10&sortBy=mostpopular&sortDirection=asc' \
                  '&term=&locationId=130154&procedureId=43482'
    base_url = 'https://www.realself.com{}'
    custom_settings = {
        'FEED_URI': 'questions_without_filter.csv',
        'FEED_FORMAT': 'csv',
        'FEED_EXPORT_ENCODING': 'utf-8',
        'FEED_EXPORT_FIELDS': ['Question Asked', 'Date Question Asked', 'Posters Location', 'Text of Question',
                               'Question Header']
    }
    headers = {
        'authority': 'www.realself.com',
        'accept': '*/*',
        'sec-ch-ua': '"Google Chrome";v="105", "Not)A;Brand";v="8", "Chromium";v="105"',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
                      'Chrome/105.0.0.0 Safari/537.36',
        'x-requested-with': 'XMLHttpRequest',
        'X-Crawlera-Profile': 'pass',
        'X-Crawlera-Region': 'us'
    }

    def start_requests(self):
        item = {'offset': 0}
        yield scrapy.Request(url=self.request_api.format(0), callback=self.parse,
                             headers=self.headers, meta={'item': item})

    def parse(self, response):
        filter_item = response.meta['item']
        result = json.loads(response.body)
        questions = result.get('questions', [])
        if questions:
            for question in questions:
                item = dict()
                item['Question Asked'] = question.get('title', '')
                item['Question Header'] = question.get('title', '')
                detail_url = question.get('uri', '')
                if not detail_url.startswith(self.base_url):
                    detail_url = self.base_url.format(detail_url)
                if detail_url:
                    yield scrapy.Request(url=detail_url, callback=self.detail_data,
                                         meta={'item': item}, headers=self.headers)
                else:
                    yield item
            # totalResults = result.get('totalResults', '')
            offset = filter_item.get('offset', '')
            for index in range(1, 220):
                offset = offset + 10
                yield scrapy.Request(url=self.request_api.format(offset),
                                     meta={'item': filter_item}, callback=self.parse,
                                     headers=self.headers)

    def detail_data(self, response):
        item = response.meta['item']
        location = response.css('div.content-subheader_individualContentSubHeaderSecondLine__nDTOi '
                                ':nth-child(3)::text').getall()
        if location:
            if len(location) > 1:
                item['Posters Location'] = location[1]
        else:
            item['Posters Location'] = ''
        item['Date Question Asked'] = response.xpath(
            '//div[@class="content-subheader_subHeader__pIFBP"]/span/text()').get('').strip()
        item['Text of Question'] = response.xpath('//div[@class="question-overview_question__JY52_"]/p/text()').get(
            '').strip()
        yield item
