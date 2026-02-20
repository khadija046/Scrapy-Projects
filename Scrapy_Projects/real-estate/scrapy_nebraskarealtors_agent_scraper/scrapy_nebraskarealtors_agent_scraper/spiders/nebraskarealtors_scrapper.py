import re

import scrapy


class NebraskarealtorsScrapperSpider(scrapy.Spider):
    name = 'nebraskarealtors_scrapper'
    requests_url = 'https://nra.rapams.com/scripts/mgrqispi.dll'
    base_url = 'https://nra.rapams.com{}'
    custom_settings = {
        'FEED_URI': 'nebraskarealtors_details.csv',
        'FEED_FORMAT': 'csv',
        'FEED_EXPORT_ENCODING': 'utf-8',
    }
    first_name = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't'
        , 'u', 'v', 'w', 'x', 'y', 'z']
    headers = {
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,'
                  'application/signed-exchange;v=b3;q=0.9',
        'Accept-Language': 'en-US,en;q=0.9',
        'Connection': 'keep-alive',
        'Content-Type': 'application/x-www-form-urlencoded',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
                      'Chrome/105.0.0.0 Safari/537.36',
        'sec-ch-ua': '"Google Chrome";v="105", "Not)A;Brand";v="8", "Chromium";v="105"',
    }

    def start_requests(self):
        for first in self.first_name:
            payload = 'APPNAME=IMS&PRGNAME=IMSAgentsandOffices&ARGUMENTS=-A241043033%2C-N2%2CLastName%2C(' \
                      'P)%2BAgent%2BNickname%2C(P)%2BOffice%2BName%2C(P)%2BCity%2C(' \
                      'P)%2BZip%2BCode&Search_Type=A&LastName=&(P)%2BAgent%2BNickname=' + first + '&(P)%2BOffice' \
                                                                                                  '%2BName=&(' \
                                                                                                  'P)%2BCity=&(' \
                                                                                                  'P)%2BZip%2BCode= '
            yield scrapy.Request(url=self.requests_url, method='POST', callback=self.parse,
                                 body=payload, headers=self.headers)

    def parse(self, response):
        for data in response.css('table.table-striped tr td:nth-child(1)'):
            detail_url = data.css('a::attr(href)').get()
            if not detail_url.startswith(self.base_url):
                detail_url = self.base_url.format(detail_url)
            name = data.css('a::text').get()
            item = {
                'First Name': name.split(',')[-1],
                'Last Name': name.split(' ')[0],
                'Source_URL': 'https://www.nebraskarealtors.com/',
                'Lead_Source': 'nebraskarealtors',
                'Occupation': 'Realtor',
                'Detail_Url': detail_url,
                'Description': '',
                'Category': '',
                'Rating': '',
                'Reviews': '',
                'Services': '',
                'Latitude': '',
                'Longitude': '',
                'Phone_Type': '',
            }
            yield scrapy.Request(url=detail_url, meta={'item': item},
                                 callback=self.parse_details, headers=self.headers)

    def parse_details(self, response):
        item = response.meta['item']
        item['Phone Number'] = response.xpath('//table[contains(@class, '
                                              '"table")]//tr/following::tr/td/following::td/text()').get().replace("(",
                                                                                                                   '').strip(),
        item['Phone Number 1'] = response.xpath('//table[contains(@class, '
                                                '"table")]//tr/following::tr/following::tr/td/following::td/text('
                                                ')').get('').strip(),
        item['Street Address'] = response.xpath(
            '//table[contains(@class, "table")]//tr/*/br/following::text()').get().strip()
        state_abb = response.xpath(
            '//table[contains(@class, "table")]//tr/*/br/following::br/following::text()').get().strip()
        if len(state_abb.split(',')) > 1:
            item['State'] = state_abb.split(',')[0]
            item['State_Abrv'] = state_abb.split(',')[-1]
        zip_check = response.xpath('//table[contains(@class, "table")]//tr/*/br/following::br/following::br'
                                   '/following::text()').get().strip()
        RE_D = re.compile(r'\d+')
        res = RE_D.search(zip_check)
        if res:
            item['Zip'] = zip_check
        else:
            item['Zip'] = ''
        item['Business Name'] = response.css('table.table-striped tr td:nth-child(2) a::text').get()
        item['Business_Site'] = response.xpath('//table[contains(@class, "table")]/*//td/a[contains(text(), '
                                               '"www")]/text()').get('')
        email = response.xpath('//table[contains(@class, "table")]/*//td/a[contains(text(), "@")]/text()').get('')
        if '@' in email:
            item['Email'] = email
        else:
            item['Email'] = ' '
        item['Full Name'] = response.css('h2.memberName::text').get()
        item['Social_Media'] = ''
        item['State_TZ'] = ''
        item['State_Type'] = ''
        item['SIC_Sectors'] = ''
        item['SIC_Categories'] = ''
        item['SIC_Industries'] = ''
        item['NAICS_Code'] = ''
        item['Quick_Occupation'] = ''
        yield item
