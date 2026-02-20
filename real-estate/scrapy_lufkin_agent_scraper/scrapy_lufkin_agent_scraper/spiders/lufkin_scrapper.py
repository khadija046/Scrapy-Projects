import scrapy


class LufkinScrapperSpider(scrapy.Spider):
    name = 'lufkin_scrapper'
    start_urls = ['https://www.lufkin-mls.com/agents.asp?content=agents_roster&the_letter=ALL']
    next_page = 'https://www.lufkin-mls.com/agents.asp?content=agents_roster&menu_id=0&the_letter=ALL&page={}'
    base_url = 'https://www.lufkin-mls.com/{}'
    custom_settings = {
        'FEED_URI': 'lufkin_data.csv',
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
        for data in response.css('div.agent-pod'):
            item = dict()
            full_name = data.css('.text-center h4::text').get('').strip()
            item['Full Name'] = full_name
            if len(full_name.split(' ')) > 1:
                item['First Name'] = full_name.split(' ')[0]
                item['Last Name'] = full_name.split(' ')[1]
            else:
                if len(full_name.split(' ')) > 2:
                    item['First Name'] = full_name.split(' ')[0]
                    item['Last Name'] = full_name.split(' ')[2]
            item['Phone Number'] = data.xpath('.//div[contains(text(), "(C)")]/text()').get('').strip().replace('(C) ', '')
            item['State_Abrv'] = data.xpath('.//div[contains(text(), "(C)")]/following::div/span/following::span/text()').get('')
            item['Email'] = data.xpath('.//a[contains(text(), "@")]/text()').get()
            item['Detail_Url'] = data.xpath('//a[@class="nrdsLink"]/@href').get()
            item['Business Name'] = data.css('div.agent_heading_inline::text').get('')
            item['Business_Site'] = data.xpath('.//a[contains(text(), "http")]/text()').get('')
            item['Phone Number 1'] = data.xpath('.//div[contains(text(), "(M)")]/text()').get('').strip().replace('(M) ', '')
            item['Source_URL'] = 'www.lufkin-mls.com'
            item['Occupation'] = 'Realtor'
            item['Lead_Source'] = 'lufkin-mls'
            yield item

        next_page = response.xpath('//a[contains(text(), "Last")]/@href').get()
        if next_page:
            page_no = next_page.split('=')[-1]
            for page in range(2, int(page_no) + 1):
                yield scrapy.Request(url=self.next_page.format(page), callback=self.parse, headers=self.headers)

