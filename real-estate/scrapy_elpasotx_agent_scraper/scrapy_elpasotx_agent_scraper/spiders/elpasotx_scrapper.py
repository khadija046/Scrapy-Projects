import scrapy


class ElpasotxScrapperSpider(scrapy.Spider):
    name = 'elpasotx_scrapper'
    start_urls = ['https://members.elpasotx.com/realtor-search/FindStartsWith?term=%23%21']
    base_url = 'https:{}'
    headers = {
        'authority': 'members.elpasotx.com',
        'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,'
                  'application/signed-exchange;v=b3;q=0.9',
        'accept-language': 'en-US,en;q=0.9',
        'sec-ch-ua': '"Google Chrome";v="105", "Not)A;Brand";v="8", "Chromium";v="105"',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
                      'Chrome/105.0.0.0 Safari/537.36 '
    }
    custom_settings = {
        'FEED_URI': 'elpasotx_details.csv',
        'FEED_FORMAT': 'csv',
        'FEED_EXPORT_ENCODING': 'utf-8',
    }

    def parse(self, response):
        for data in response.css('div.card'):
            full_name = data.css('a::attr(alt)').get()
            detail_url = data.css('a::attr(href)').get()
            if not detail_url.startswith(self.base_url):
                detail_url = self.base_url.format(detail_url)
            item = {
                'Business Name': data.css('span.gz-list-org-name::text').get(),
                'Full Name': full_name,
                'First Name': full_name.split(' ')[0],
                'Last Name': full_name.split(' ')[1],
                'Street Address': data.css('ul.list-group span[itemprop="streetAddress"]::text').get(''),
                'State_Abb': data.css('ul.list-group span[itemprop="addressRegion"]::text').get(''),
                'Zip': data.css('ul.list-group span[itemprop="postalCode"]::text').get(),
                'State': data.css('ul.list-group span[itemprop="addressLocality"]::text').get(),
                'Business_Site': data.css('li.gz-card-website a::attr(href)').get(),
                'Email': '',
                'Source_URL': 'https://members.elpasotx.com/',
                'Lead_Source': 'elpasotx',
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
        item['Phone Number'] = response.css('span[itemprop="telephone"]::text').get()
        item['Business_Site'] = ''
        item['Social_Media'] = ' '
        item['State_TZ'] = ''
        item['State_Type'] = ''
        item['SIC_Sectors'] = ''
        item['SIC_Categories'] = ''
        item['SIC_Industries'] = ''
        item['NAICS_Code'] = ''
        item['Quick_Occupation'] = ''
        yield item


