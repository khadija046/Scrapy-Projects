import json
from datetime import datetime

import scrapy


class BairdwarnerSpider(scrapy.Spider):
    name = 'bairdwarner'
    request_api = "http://api.kvcore.com/public/members/newlist?page=1"

    custom_settings = {
        'FEED_URI': 'bairdwarner.csv',
        'FEED_FORMAT': 'csv',
        'FEED_EXPORT_ENCODING': 'utf-8-sig',
        'FEED_EXPORT_FIELDS': ['Business Name', 'Full Name', 'First Name', 'Last Name', 'Street Address',
                               'Valid To', 'State', 'Zip', 'Description', 'Phone Number', 'Phone Number 1', 'Email',
                               'Business_Site', 'Social_Media', 'Record_Type',
                               'Category', 'Rating', 'Reviews', 'Source_URL', 'Detail_Url', 'Services',
                               'Latitude', 'Longitude', 'Occupation',
                               'Business_Type', 'Lead_Source', 'State_Abrv', 'State_TZ', 'State_Type',
                               'SIC_Sectors', 'SIC_Categories',
                               'SIC_Industries', 'NAICS_Code', 'Quick_Occupation', 'Scraped_date', 'Meta_Description']
    }

    headers = {
        'authority': 'api.kvcore.com',
        'accept': 'application/json, text/javascript, */*; q=0.01',
        'accept-language': 'en-GB,en-US;q=0.9,en;q=0.8',
        'authorization': 'b5764ab7-8c23-4cff-97a0-bfbee3158dd5',
        'origin': 'https://www.bairdwarner.com',
        'referer': 'https://www.bairdwarner.com/',
        'sec-ch-ua': '"Google Chrome";v="107", "Chromium";v="107", "Not=A?Brand";v="24"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"Windows"',
        'sec-fetch-dest': 'empty',
        'sec-fetch-mode': 'cors',
        'sec-fetch-site': 'cross-site',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/107.0.0.0 Safari/537.36',
        'Cookie': '__cf_bm=t6GeJvU..AsLjpvCBvJtO.b6qCAnT1w58IxHxRewWEI-1669716601-0-AesGx6I/Xn0o4TZBgCkYPpT49WpEwS2zsexQ6qgtFGHnM2vZ3aeYGvU1yZO9nU0jxDTzw95V4tjggiyz49T2G40='
    }

    def start_requests(self):
        yield scrapy.Request(url=self.request_api, callback=self.parse, headers=self.headers)

    def parse(self, response):
        try:
            json_data = json.loads(response.body)
            for data in json_data.get('data', []):
                item = dict()
                item['First Name'] = data.get('first_name', '')
                item['Last Name'] = data.get('last_name', '')
                item['Full Name'] = item['First Name'] + ' ' + item['Last Name']
                item['Phone Number'] = data.get('direct_phone', '')
                item['Phone Number 1'] = data.get('work_phone', '')
                item['Email'] = data.get('email', '')
                item['Business_Site'] = data.get('website_url', '')
                item['Source_URL'] = 'https://www.bairdwarner.com/our_agents/'
                item['Occupation'] = data.get('title', '')
                item['Lead_Source'] = 'bairdwarner'
                item['Record_Type'] = 'Person'
                item['Meta_Description'] = "Choose from the best real estate agents in Chicagoland. Whether you’re " \
                                           "buying or selling with a Baird & Warner agent, you’ll have experience, " \
                                           "knowledge and innovation on your side. Home / Real Estate Agents"
                item['Scraped_date'] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                yield item

            next_page = json_data.get('pagination', {}).get('next_page_url', '')
            if next_page:
                yield scrapy.Request(url=next_page, callback=self.parse, headers=self.headers)
        except Exception as ex:
            print('Error From parse | ' + str(ex))

