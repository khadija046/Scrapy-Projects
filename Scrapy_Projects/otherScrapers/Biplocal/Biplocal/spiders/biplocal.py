import re
from datetime import datetime

import scrapy


class BiplocalSpider(scrapy.Spider):
    name = 'biplocal'
    start_urls = ['https://www.biplocal.com/search_results']
    custom_settings = {
        'FEED_URI': 'biplocal.csv',
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
        'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,'
                  'application/signed-exchange;v=b3;q=0.9',
        'accept-language': 'en-US,en;q=0.9',
        'sec-ch-ua': '"Google Chrome";v="105", "Not)A;Brand";v="8", "Chromium";v="105"',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
                      'Chrome/105.0.0.0 Safari/537.36 '
    }

    def parse(self, response):
        for data in response.css('div.member_results div.mid_section a.center-block'):
            detail_url = data.css('::attr(href)').get()
            if detail_url:
                yield response.follow(url=detail_url, callback=self.parse_detail, headers=self.headers)

        next_page = response.css('a[rel="next"]::attr(href)').get()
        if next_page:
            yield response.follow(url=next_page, callback=self.parse, headers=self.headers)

    def parse_detail(self, response):
        item = dict()
        item['Business Name'] = response.css('div.col-sm-10 h1.bold::text').get('').strip()
        item['Phone Number'] = response.css('div.myphoneHide a u::text').get('').strip()
        item['Business_Site'] = response.css('a.weblink::attr(href)').get('').strip()
        contact_detail = ','.join(data.xpath('./text()').get() for data in
                                  response.xpath('//div[contains(text(), "Location")]/following-sibling::div/span'))
        try:
            zip_code = re.search(r"(?!\A)\b\d{5}(?:-\d{4})?\b", contact_detail).group(0)
        except:
            zip_code = ''
        item['Zip'] = zip_code
        item['Street Address'] = response.xpath(
            '//div[contains(text(), "Location")]/following-sibling::div/span/text()[1]').get('').strip()
        state = response.css('span.profile-header-location::text').get('').strip()
        if len(state.split(',')) == 3:
            item['State'] = state.split(',')[1].strip()
        item['Source_URL'] = 'https://www.biplocal.com/search_results'
        item['Occupation'] = response.css('span.profile-header-top-category ::text').get('').strip()
        item['Lead_Source'] = 'biplocal'
        item['Detail_Url'] = response.url
        item['Record_Type'] = 'Business'
        item['Meta_Description'] = "Search our Local Business Directory database and connect with top rated Local " \
                                   "Businesses."
        item['Scraped_date'] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        yield item
