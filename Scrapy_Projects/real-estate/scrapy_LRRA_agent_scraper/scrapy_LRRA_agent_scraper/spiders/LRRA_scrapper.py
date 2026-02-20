import json

import scrapy


class LrraScrapperSpider(scrapy.Spider):
    name = 'LRRA_scrapper'
    request_url = 'https://www.realtor.com/realestateagents/agentname-{}'
    base_url = 'https://www.realtor.com{}'
    first_name = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't'
        , 'u', 'v', 'w', 'x', 'y', 'z']
    last_name = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't',
                 'u', 'v', 'w', 'x', 'y', 'z']
    custom_settings = {
        'FEED_URI': 'LRRA_data.csv',
        'FEED_FORMAT': 'csv',
        'FEED_EXPORT_ENCODING': 'utf-8-sig',
        'FEED_EXPORT_FIELDS': ['Business Name', 'Full Name', 'First Name', 'Last Name', 'Street Address',
                               'State', 'Zip', 'Description', 'Phone Number', 'Phone Number 1', 'Email',
                               'Business_Site', 'Social_Media',
                               'Category', 'Rating', 'Reviews', 'Source_URL', 'Detail_Url', 'Services',
                               'Latitude', 'Longitude', 'Occupation',
                               'Phone_Type', 'Lead_Source', 'State_Abrv', 'State_TZ', 'State_Type',
                               'SIC_Sectors', 'SIC_Categories',
                               'SIC_Industries', 'NAICS_Code', 'Quick_Occupation']

    }
    headers = {
        'authority': 'www.realtor.com',
        'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,'
                  'application/signed-exchange;v=b3;q=0.9',
        'accept-language': 'en-US,en;q=0.9',
        'if-none-match': '"becfb-AQPzxeTgCvee++Rz+V2Hq2c7P48"',
        'sec-ch-ua': '"Google Chrome";v="105", "Not)A;Brand";v="8", "Chromium";v="105"',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
                      'Chrome/105.0.0.0 Safari/537.36 '
    }

    def start_requests(self):
        for first in self.first_name:
            for last in self.last_name:
                req_url = {'url': self.request_url.format(first + last)}
                yield scrapy.Request(url=self.request_url.format(first + last), meta={'url': req_url},
                                     callback=self.parse, headers=self.headers)

    def parse(self, response):
        req_url = response.meta['url']
        for data in response.css('div.agent-list-card'):
            detail_url = data.css('div.agent-list-card .col-xxs-4 a.jsx-3970352998::attr(href)').get()
            if detail_url:
                if not detail_url.startswith(self.base_url):
                    detail_url = self.base_url.format(detail_url)
                yield scrapy.Request(url=detail_url, callback=self.parse_data, headers=self.headers)

        total_pages = response.css('div[aria-label="pagination"] a:nth-child(8)::text').get('')
        if total_pages:
            for next_id in range(2, int(total_pages) + 1):
                yield scrapy.Request(url=req_url.get('url', '') + '/pg-' + str(next_id), meta={'url': req_url},
                                     callback=self.parse, headers=self.headers)

    def parse_data(self, response):
        json_obj = response.css('script[type = "application/json"]::text').get()
        if json_obj:
            result = json.loads(json_obj)
            data = result.get('props', {}).get('pageProps', {}).get('jsonld', {}).get('content', {})
            if data:
                item = dict()
                item['Full Name'] = data.get('agentName', '')
                if data.get('firstName', ''):
                    if data.get('lastName', ''):
                        item['First Name'] = data.get('firstName', '')
                        item['Last Name'] = data.get('lastName', '')
                else:
                    full_name = data.get('agentName', '').split(' ')
                    if len(full_name) > 1:
                        item['First Name'] = full_name[0]
                        item['Last Name'] = full_name[1]
                item['Phone Number'] = data.get('telephone', '')
                item['Business Name'] = data.get('officeName', '')
                item['Source_URL'] = 'https://www.lrra.com/'
                item['Occupation'] = 'Realtor'
                item['Detail_Url'] = data.get('url', '')
                item['Lead_Source'] = 'lrra'
                item['Description'] = data.get('description', '')
                item['Street Address'] = data.get('location', '').get('line', '')
                item['State_Abrv'] = data.get('location', '').get('state', '')
                item['Zip'] = data.get('location', '').get('postal_code', '')
                item['Rating'] = data.get('averagegRating', '').get('reviewCount', '')
                yield item
