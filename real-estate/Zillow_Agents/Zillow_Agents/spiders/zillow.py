import csv
import json
from typing import Iterable

import scrapy
from scrapy import Request


class ZillowSpider(scrapy.Spider):
    name = "zillow"
    url = "https://www.zillow.com/professionals/real-estate-agent-reviews/{}/?page={}"
    headers = {
        'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
        'accept-language': 'en-GB,en-US;q=0.9,en;q=0.8',
        'cache-control': 'max-age=0',
        'priority': 'u=0, i',
        'sec-ch-ua': '"Google Chrome";v="137", "Chromium";v="137", "Not/A)Brand";v="24"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"Windows"',
        'sec-fetch-dest': 'document',
        'sec-fetch-mode': 'navigate',
        'sec-fetch-site': 'same-origin',
        'upgrade-insecure-requests': '1',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/137.0.0.0 Safari/537.36',
        'Cookie': '_gcl_au=1.1.107016058.1746117459; _scid=uOmzbbCpA_bAxQO2n3S7abV-f-ktf7BmWmzIpA; _tt_enable_cookie=1; _ttp=01JT6BC29WE0K4BBWESNJFWS9W_.tt.1; _pin_unauth=dWlkPU5EQTRaV1V3WVdNdE1UQXhNeTAwT1RjMExXSTROamt0T0RrM1lqUmpNMlpsWVdFMw; optimizelyEndUserId=oeu1746983554936r0.7190330226835719; zgcus_aeut=AEUUT_225c2060-2e8b-11f0-8022-d2e0d5428d93; zgcus_aeuut=AEUUT_225c2060-2e8b-11f0-8022-d2e0d5428d93; optimizelySession=1746983556713; kn_cs_visitor_id=1ca15839-c54d-447f-9190-caa0c5d3536d; fs_uid=#o-21MVN0-na1#1db247d6-59ae-47dc-9e1c-c84b97b3ec02:2d01068b-ba77-449a-b7f1-3ba19566bf87:1746983557568::1#/1778519559; search=6|1749968330585%7Crect%3D48.225697397616976%2C-79.89841015771485%2C48.09561899267589%2C-80.16826184228516%26rid%3D792527%26disp%3Dmap%26mdm%3Dauto%26p%3D1%26listPriceActive%3D1%26fs%3D1%26fr%3D0%26mmm%3D0%26rs%3D0%26singlestory%3D0%26housing-connector%3D0%26parking-spots%3Dnull-%26abo%3D0%26garage%3D0%26pool%3D0%26ac%3D0%26waterfront%3D0%26finished%3D0%26unfinished%3D0%26cityview%3D0%26mountainview%3D0%26parkview%3D0%26waterview%3D0%26hoadata%3D1%26zillow-owned%3D0%263dhome%3D0%26showcase%3D0%26featuredMultiFamilyBuilding%3D0%26onlyRentalStudentHousingType%3D0%26onlyRentalIncomeRestrictedHousingType%3D0%26onlyRentalMilitaryHousingType%3D0%26onlyRentalDisabledHousingType%3D0%26onlyRentalSeniorHousingType%3D0%26commuteMode%3Ddriving%26commuteTimeOfDay%3Dnow%09%09792527%09%7B%22isList%22%3Atrue%2C%22isMap%22%3Atrue%7D%09%09%09%09%09; zguid=24|%2498c3742d-6bed-4c46-94f2-5792a328dfed; zgsession=1|2abafdc0-1edd-4f44-85e7-10da491c4728; _ga=GA1.2.1480614637.1750607006; zjs_anonymous_id=%2298c3742d-6bed-4c46-94f2-5792a328dfed%22; zjs_user_id=null; zg_anonymous_id=%22c08eaec0-8ebc-4248-8fd8-38783a0a2f33%22; zjs_user_id_type=%22encoded_zuid%22; pxcts=a588343e-4f7f-11f0-9c32-eef35debc57b; _pxvid=a588282d-4f7f-11f0-9c32-f771ee1c0372; _ScCbts=%5B%22299%3Bchrome.2%3A2%3A5%22%2C%22309%3Bchrome.2%3A2%3A5%22%5D; DoubleClickSession=true; _sctr=1%7C1750532400000; _gid=GA1.2.1638204373.1750750522; JSESSIONID=A6984BDD40A440720C0DB80EAAFA7442; _clck=1e1ax1t%7C2%7Cfx1%7C0%7C1947; AWSALB=JQRb7Smfz0k0uUCSqZklIOyrT6kGScu/SMmVu3fSsClsbOtIQa/+06LRXsfKAuPWLDAHuxPtrxQvA47JMo0mFLUq0W5jUoxWtbMMfI51TdN6BZLftct3J5oW6SUe; AWSALBCORS=JQRb7Smfz0k0uUCSqZklIOyrT6kGScu/SMmVu3fSsClsbOtIQa/+06LRXsfKAuPWLDAHuxPtrxQvA47JMo0mFLUq0W5jUoxWtbMMfI51TdN6BZLftct3J5oW6SUe; _rdt_uuid=1736787388433.f56105cb-2518-4272-8f96-c5f237c2746e; _scid_r=sumzbbCpA_bAxQO2n3S7abV-f-ktf7BmWmzIvQ; ttcsid=1750750539434::9Iand_-xJK-lJCjT2a2P.6.1750752726079; _uetsid=d284093050cd11f0a22bf78f4d4fd506; _uetvid=568a1320d1cf11ef85f7b95d71341513; _clsk=1jigii3%7C1750752731223%7C8%7C0%7Cy.clarity.ms%2Fcollect; ttcsid_CN5P33RC77UF9CBTPH9G=1750750539433::JbiNg_pmddr_tWkpPsKW.6.1750752733971; web-platform-data=%7B%22wp-dd-rum-session%22%3A%7B%22expire%22%3A1750753635789%7D%7D; _px3=aa61c5aba39d849d14567dc12bde2df44a2beef8ecebfecfbe27958d5a8d22bb:rP2IlnPJSTKVnJnYFSXaeavSSfdJxeFYffbFWDN6OxfXoP9JOYxH2rBeo2u5hMphcohWMtzp0CC7HOP7q0AxHg==:1000:lPB40pk32oOUa7199/PgOooKRIyWoRNoF0rYw1UoB8H7FgbyxeBmakhmZnRUjE085C0pfC2FH2zhtLj2VXwr/6BWZo7no7bu0evhWE9SM0iNx0t2aDzyXCuqsFdc+Af7dTSdvjcVHSqFAQQknjR2oNLugrn5yzjc2bMlO358xqF9j+G/smGaTY5fqKRce9JKY2Rv3BAHviHzo51a90/2aoks34ZwfbZruwYo1GcZVZw=; search=6|1749803634374%7Crect%3D40.973190668392284%2C-72.90027426171878%2C40.42136971824492%2C-75.05908773828128%26rid%3D6181%26disp%3Dmap%26mdm%3Dauto%26p%3D3%26listPriceActive%3D1%26fs%3D1%26fr%3D0%26mmm%3D0%26rs%3D0%26singlestory%3D0%26housing-connector%3D0%26parking-spots%3Dnull-%26abo%3D0%26garage%3D0%26pool%3D0%26ac%3D0%26waterfront%3D0%26finished%3D0%26unfinished%3D0%26cityview%3D0%26mountainview%3D0%26parkview%3D0%26waterview%3D0%26hoadata%3D1%26zillow-owned%3D0%263dhome%3D0%26showcase%3D0%26featuredMultiFamilyBuilding%3D0%26onlyRentalStudentHousingType%3D0%26onlyRentalIncomeRestrictedHousingType%3D0%26onlyRentalMilitaryHousingType%3D0%26onlyRentalDisabledHousingType%3D0%26onlyRentalSeniorHousingType%3D0%26commuteMode%3Ddriving%26commuteTimeOfDay%3Dnow%09%096181%09%7B%22isList%22%3Atrue%2C%22isMap%22%3Atrue%7D%09%09%09%09%09'
    }
    custom_settings = {
        'FEED_URI': f'outputs/zillow_data_sample_1.csv',
        'FEED_FORMAT': 'csv',
        'FEED_EXPORT_ENCODING': 'utf-8',
        'HTTPERROR_ALLOWED_CODES': [404]
    }

    def read_csv(self):
        with open('input/counties.csv', 'r') as csvFile:
            return list(csv.DictReader(csvFile))

    def start_requests(self) -> Iterable[Request]:
        request_area = self.read_csv()
        for area in request_area[:]:
            county = area.get('county', '')
            state = area.get('state', '')
            query = f"{county.replace(' ', '-').lower()}-{state.lower()}"
            raw_url = self.url.format(query, '1')
            yield scrapy.Request(url=raw_url, headers=self.headers, meta={'current': 1, 'query':query})


    def parse(self, response):
        for agents in response.css('a.PSeQE')[:]:
            agent_url = agents.css('::attr(href)').get('').strip()
            yield scrapy.Request(url=agent_url, headers=self.headers, callback=self.parse_agents)

        next_page = response.css('button[title="Next page"]::attr(aria-disabled)').get('').strip()
        if next_page == 'false':
            current_page = response.meta['current']
            query = response.meta['query']
            next_page = current_page + 1
            yield scrapy.Request(url=self.url.format(query, next_page), headers=self.headers,
                                 meta={'current': next_page, 'query': query}, callback=self.parse)


    def parse_agents(self, response):
        script_data = json.loads(response.css('script#__NEXT_DATA__::text').get('').strip())
        propsPage = script_data.get('props', {}).get('pageProps', {}).get('displayUser', {})
        item = dict()
        item['Name'] = propsPage.get('name', '')
        item['businessName'] = propsPage.get('businessName', '')
        businessAddress = propsPage.get('businessAddress', {})
        item['address1'] = businessAddress.get('address1', '')
        item['address2'] = businessAddress.get('address2', '')
        item['city'] = businessAddress.get('city', '')
        item['state'] = businessAddress.get('state', '')
        item['postalCode'] = businessAddress.get('postalCode', '')
        item['isPremierAgent'] = propsPage.get('isPremierAgent', '')
        phoneNumbers = propsPage.get('phoneNumbers', {})
        item['Mobile Number'] = phoneNumbers.get('cell', '')
        item['Business Number'] = phoneNumbers.get('business', '')
        item['email'] = propsPage.get('email', '')
        item['url'] = response.url
        yield item
