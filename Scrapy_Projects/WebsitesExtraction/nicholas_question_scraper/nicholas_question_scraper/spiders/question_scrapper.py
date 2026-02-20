import json

import scrapy


class QuestionScrapperSpider(scrapy.Spider):
    name = 'question_scrapper'
    request_api = 'https://www.realself.com/questionslist/43482/topicFilter?emptyAnswers=false&showQuestions=1&offset' \
                  '=0&limit=10&sortBy=mostpopular&sortDirection=asc&term=&locationId=130154&tags=8497'
    page_api = 'https://search.realself.com/questions-api?showQuestions={}&offset={}&limit=10&sortBy=mostpopular' \
               '&sortDirection=asc&term=&locationId=29589&procedureId=43482&tags={}'
    base_url = 'https://www.realself.com{}'
    custom_settings = {
        'FEED_URI': 'questions_detail_before.csv',
        'FEED_FORMAT': 'csv',
        'FEED_EXPORT_ENCODING': 'utf-8',
        'FEED_EXPORT_FIELDS': ['Question Asked', 'Date Question Asked', 'Posters Location', 'Text of Question',
                               'Question Header', 'Question Type', 'Tag']
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
        yield scrapy.Request(url=self.request_api, callback=self.get_filter_data,
                             headers=self.headers)

    def get_filter_data(self, response):
        result = json.loads(response.body)
        filters = result.get('filters', {})
        show_question = dict()
        tags = dict()
        ages = dict()
        for filtr in filters.get('showQuestions', []):
            if filtr.get('id', '') == 3:
                pass
            else:
                show_question[filtr.get('id', '')] = filtr.get('name', '')
        for tag in filters.get('tags', []):
            tags[tag.get('id', '')] = tag.get('name', '')
        for age_fil in filters.get('age', []):
            ages[age_fil.get('id', '')] = age_fil.get('name', '')

        # for question in show_question.keys():
        for tag in tags.keys():
            item = {
                'question': 'Before Procedure Only',
                'tag': tags[tag],
                'offset': 0,
                'q_id': '1',
                'tag_id': tag
            }
            yield scrapy.Request(url=self.page_api.format('1', 0, tag), meta={'item': item},
                                 callback=self.parse, headers=self.headers)

    def parse(self, response):
        filter_item = response.meta['item']
        result = json.loads(response.body)
        questions = result.get('questions', [])
        if questions:
            for question in questions:
                item = dict()
                item['Question Asked'] = question.get('title', '')
                item['Question Header'] = question.get('title', '')
                item['Question Type'] = filter_item.get('question', '')
                item['Tag'] = filter_item.get('tag', '')
                detail_url = question.get('uri', '')
                if not detail_url.startswith(self.base_url):
                    detail_url = self.base_url.format(detail_url)
                if detail_url:
                    yield scrapy.Request(url=detail_url, callback=self.detail_data,
                                         meta={'item': item}, headers=self.headers)
                else:
                    yield item
            totalResults = result.get('totalResults', '')
            offset = filter_item.get('offset', '')
            for index in range(1, int(int(totalResults) / 10) + 1):
                offset = offset + 10
                yield scrapy.Request(url=self.page_api.format(filter_item.get('q_id', ''), offset,
                                                              filter_item.get('tag_id', '')),
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
