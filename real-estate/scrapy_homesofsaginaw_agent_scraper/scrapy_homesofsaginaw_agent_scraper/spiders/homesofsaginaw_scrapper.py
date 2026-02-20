import scrapy


class HomesofsaginawScrapperSpider(scrapy.Spider):
    name = 'homesofsaginaw_scrapper'
    start_urls = ['https://www.homesofsaginaw.com/realtors.cfm?LastName=&search=yes']
    base_url = 'https://www.homesofsaginaw.com/{}'
    custom_settings = {
        'FEED_URI': 'homesofsaginaw_data.csv',
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
        'authority': 'www.homesofsaginaw.com',
        'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,'
                  'application/signed-exchange;v=b3;q=0.9',
        'accept-language': 'en-US,en;q=0.9',
        'sec-ch-ua': '"Google Chrome";v="105", "Not)A;Brand";v="8", "Chromium";v="105"',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
                      'Chrome/105.0.0.0 Safari/537.36 '
    }

    def parse(self, response):
        for data in response.xpath('//div[contains(@class, "col-md-push-3")]/p/a'):
            url = data.xpath('./@href').get()
            if not url.startswith(self.base_url):
                url = self.base_url.format(url)
            yield scrapy.Request(url=url, callback=self.parse_data, headers=self.headers)

    def parse_data(self, response):
        for data in response.css('div.col-xs-9'):
            full_name = data.css('h2::text').get()
            item = dict()
            item['Full Name'] = full_name
            item['First Name'] = full_name.split(',')[1].strip()
            item['Last Name'] = full_name.split(',')[0]
            item['Business Name'] = data.css('h5::text').get('').strip()
            item['Phone Number'] = data.xpath('.//b[contains(text(), "Phone")]/following::text()').get('').strip()
            item['Email'] = data.xpath('.//a[contains(text(), "@")]/text()').get('')
            item['Business_Site'] = data.xpath('.//a[contains(text(), "www")]/@href').get('')
            item['Source_URL'] = 'www.homesofsaginaw.com'
            item['Occupation'] = 'Realtor'
            item['Lead_Source'] = 'homesofsaginaw'
            yield item
