import scrapy


class SbarearealtorsScrapperSpider(scrapy.Spider):
    name = 'sbarearealtors_scrapper'
    base_url = 'https://www.reindiana.com{}'
    request_url = 'https://www.reindiana.com/agentsearch/results.aspx?SearchType=agent&FirstName={}&LastName' \
                  '=&OfficeName=&Address=&City=&State=&Country=-32768&Zip=&Languages=&Titles=&Specialties' \
                  '=&Accreditations=&Areas=&rpp=50&page={}&SortOrder= '
    first_name = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't'
        , 'u', 'v', 'w', 'x', 'y', 'z']

    custom_settings = {
        'FEED_URI': 'sbarearealtors_data.csv',
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
        'authority': 'www.reindiana.com',
        'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,'
                  'application/signed-exchange;v=b3;q=0.9',
        'accept-language': 'en-US,en;q=0.9',
        'sec-ch-ua': '"Google Chrome";v="105", "Not)A;Brand";v="8", "Chromium";v="105"',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
                      'Chrome/105.0.0.0 Safari/537.36 '
    }

    def start_requests(self):
        for first in self.first_name:
            alpha = {'alpha': first}
            yield scrapy.Request(url=self.request_url.format(first, '1'), meta={'alpha': alpha},
                                 callback=self.parse, headers=self.headers)

    def parse(self, response):
        alpha = response.meta['alpha']
        for data in response.css('div.rui-row'):
            detail_url = data.css('h3 a::attr(href)').get()
            if not detail_url.startswith(self.base_url):
                detail_url = self.base_url.format(detail_url)
            full_name = data.css('h3 a::text').get('')
            item = dict()
            item['Business Name'] = data.css('.ao-office a::text').get()
            item['Full Name'] = full_name
            item['First Name'] = full_name.split(' ')[0]
            item['Last Name'] = full_name.split(' ')[1]
            item['Street Address'] = data.css('span.ao-address::text').get()
            item['Phone Number'] = data.xpath('.//span[contains(text(),"Office:")]/following::text()').get('').strip()
            address = data.xpath('.//span[@class="ao-address"]/following::text()').get('').strip()
            if len(address.split(',')) > 1:
                new_address = address.split(',')[-1]
                item['State'] = new_address.split(' ')[1]
                item['Zip'] = new_address.split(' ')[2]
            item['Phone Number 1'] = data.css('div[id="ao-cell"]::text').get('').replace('Mobile: ', '')
            item['Source_URL'] = 'https://sbarearealtors.org/'
            item['Detail_Url'] = detail_url
            item['Occupation'] = 'Realtor'
            item['Lead_Source'] = 'sbarearealtors'

            yield scrapy.Request(url=detail_url, meta={'item': item}, callback=self.parse_data, headers=self.headers)

        total_data = response.css('td[align="center"] span.ao_page_controls_text::text').get('').split(' ')[-1]
        total = int(total_data) / 50 + 1
        for next_page in range(2, int(total)):
            yield scrapy.Request(url=self.request_url.format(alpha.get('alpha', ''), next_page), meta={'alpha': alpha},
                                 callback=self.parse, headers=self.headers)

    def parse_data(self, response):
        item = response.meta['item']
        item['Email'] = response.css('a[id="hlAgentEmailAddress"]::text').get()
        yield item
