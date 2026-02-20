import scrapy


class RecoloradoScrapperSpider(scrapy.Spider):
    name = 'recolorado_scrapper'
    start_urls = ['https://www.recolorado.com/agents']
    page_url = 'https://www.recolorado.com/agents.html?results={}'
    custom_settings = {
        'FEED_URI': 'recolorado_details.csv',
        'FEED_FORMAT': 'csv',
        'FEED_EXPORT_ENCODING': 'utf-8',
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
        for data in response.xpath('//div[@class="agent-cards"]/div[contains(@class,"agent-card")]'):
            full_name = data.xpath('.//*/div[@class="agent-name"]/a/text()').get()
            detail_url = data.xpath('.//*/div[@class="agent-name"]/a/@href').get()
            item = {
                'Business Name': data.xpath('.//*/div[@class="agent-office-name"]/text()').get(),
                'Full Name': full_name,
                'First Name': full_name.split(' ')[0],
                'Last Name': full_name.split(' ')[-1],
                'Phone Number': data.xpath('.//div[@class="agent-office-number"]/a/span[contains(text(), '
                                           '"Office:")]/following-sibling::text()').get('').strip(),
                'Phone Number 1': data.xpath('.//div[@class="agent-cards"]/div[contains(@class,'
                                             '"agent-card")]//div[@class="agent-office-number"]/a/span[contains('
                                             'text(),"Direct:")]/following-sibling::text()').get('').strip(),
                'Email': data.xpath('.//*/div[@class="agent-email"]/a/@data-email').get(),
                'Source_URL': 'https://www.recolorado.com/',
                'Lead_Source': 'recolorado',
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

        total_pages = response.css('ul.pagination::attr(data-pages)').get()
        current_page = response.css('ul.pagination::attr(data-current-page)').get()
        next_page = int(current_page) + 1
        if next_page <= int(total_pages):
            yield scrapy.Request(url=self.page_url.format(next_page), callback=self.parse, headers=self.headers)

    def parse_details(self, response):
        item = response.meta['item']
        address = response.css('div.agent-details-header-office-address::text').get('').strip()
        address_list = address.split(',')
        if len(address_list) > 1:
            item['Street Address'] = address_list[0]
            item['State'] = address_list[1]
            item['Zip'] = address_list[2]
        item['Business_Site'] = response.css('div.agent-details-header-website-url a::attr(href)').get('')
        item['Social_Media'] = ', '.join(url.css('::attr(href)').get() for url in response.css('div.agent-details'
                                                                                               '-header-social a'))
        item['State_TZ'] = ''
        item['State_Type'] = ''
        item['SIC_Sectors'] = ''
        item['SIC_Categories'] = ''
        item['SIC_Industries'] = ''
        item['NAICS_Code'] = ''
        item['Quick_Occupation'] = ''
        yield item
