import copy
import json

import scrapy


class GpbrScrapperSpider(scrapy.Spider):
    name = 'GPBR_scrapper'
    request_api = 'https://mdweb.mmsi2.com/webapi/gpbr/index.php/roster_search'
    first_name = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't',
                  'u', 'v', 'w', 'x', 'y', 'z']
    custom_settings = {
        'FEED_URI': 'GPBR_data.csv',
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
    payload = {"search_type": "Individual Member", "first_name": "a"}
    headers = {
        'Accept': 'application/json, text/plain, */*',
        'Accept-Language': 'en-US,en;q=0.9',
        'Connection': 'keep-alive',
        'Content-Type': 'application/json;charset=UTF-8',
        'Origin': 'https://mdweb.mmsi2.com',
        'Referer': 'https://mdweb.mmsi2.com/gpbr/roster/',
        'Sec-Fetch-Dest': 'empty',
        'Sec-Fetch-Mode': 'cors',
        'Sec-Fetch-Site': 'same-origin',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/105.0.0.0 Safari/537.36',
        'sec-ch-ua': '"Google Chrome";v="105", "Not)A;Brand";v="8", "Chromium";v="105"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"Windows"'
    }

    def start_requests(self):
        for first in self.first_name:
            payload = copy.deepcopy(self.payload)
            payload['first_name'] = first
            yield scrapy.Request(url=self.request_api, method='POST', callback=self.parse,
                                 body=json.dumps(payload), headers=self.headers)

    def parse(self, response):
        if response.body:
            result = json.loads(response.body)
            item = dict()
            for data in result:
                full_name = data.get('NAME', '')
                item['Full Name'] = full_name
                item['First Name'] = full_name.split(',')[0]
                item['Last Name'] = full_name.split(',')[1].strip()
                item['Business Name'] = data.get('FIRM_NAME', '')
                item['Street Address'] = data.get('FIRM_ADDRESS_1', '')
                item['State_Abrv'] = data.get('FIRM_STATE', '')
                item['Zip'] = data.get('FIRM_ZIP', '')
                item['Phone Number'] = data.get('PREF_PHONE', '')
                item['Phone Number 1'] = data.get('CELL_PHONE', '')
                item['Email'] = data.get('EMAIL', '')
                item['Source_URL'] = 'www.GPBR.com'
                item['Occupation'] = 'Realtor'
                item['Lead_Source'] = 'GPBR'
                yield item

