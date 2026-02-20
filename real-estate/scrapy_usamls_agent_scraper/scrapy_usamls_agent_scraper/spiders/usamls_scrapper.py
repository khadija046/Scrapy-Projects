import scrapy


class UsamlsScrapperSpider(scrapy.Spider):
    name = 'usamls_scrapper'
    start_urls = ['https://www.usamls.net/ncentral/default.asp?content=agents&the_letter=ALL']
    base_url = 'https://www.usamls.net/ncentral/{}'
    custom_settings = {
        'FEED_URI': 'usamls_data.csv',
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
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,'
                  'application/signed-exchange;v=b3;q=0.9',
        'Accept-Language': 'en-US,en;q=0.9',
        'Connection': 'keep-alive',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
                      'Chrome/105.0.0.0 Safari/537.36',
        'sec-ch-ua': '"Google Chrome";v="105", "Not)A;Brand";v="8", "Chromium";v="105"',
    }

    def parse(self, response):
        for data in response.css('.agent_inside_link tr'):
            detail_url = data.css('td:nth-child(1) a.nrdsLink::attr(href)').get()
            item = dict()
            full_name = data.css('td:nth-child(1) .agent_heading_inline::text').get()
            item['Full Name'] = full_name
            item['First Name'] = full_name.split(' ')[0]
            item['Last Name'] = full_name.split(' ')[1]
            item['Phone Number'] = data.xpath('.//td/div[contains(text(), "(C)")]/text()').get('').replace('(C) ',
                                                                                                           '').strip()
            item['Phone Number 1'] = data.xpath('.//td/div[contains(text(), "(M)")]/text()').get('').replace('(M) ',
                                                                                                             '').strip()
            item['Email'] = data.xpath('.//td[@width="48%"]//a[contains(text(), "@")]/text()').get()
            item['Business Name'] = data.css('td:nth-child(2) .agent_heading_inline::text').get()
            item['Source_URL'] = 'www.usamls.net/ncentral'
            item['Occupation'] = 'Realtor'
            item['Detail_Url'] = detail_url
            item['Lead_Source'] = 'usamls'
            if detail_url:
                yield scrapy.Request(url=detail_url, meta={'item': item},
                                     callback=self.parse_data, headers=self.headers)
            else:
                yield item

        next_page = response.xpath('//div[@class="agent_return_pages"]/a[contains(text(), "[Next >>]")]/@href').get()
        if next_page:
            if not next_page.startswith(self.base_url):
                next_page = self.base_url.format(next_page)
            yield scrapy.Request(url=next_page, callback=self.parse, headers=self.headers)

    def parse_data(self, response):
        item = response.meta['item']
        item['Street Address'] = response.css('p.agent_address span:nth-child(1)::text').get('').strip()
        item['State'] = response.css('p.agent_address span:nth-child(2)::text').get('').strip()
        item['Zip'] = response.css('p.agent_address span:nth-child(4)::text').get('').strip()
        yield item
