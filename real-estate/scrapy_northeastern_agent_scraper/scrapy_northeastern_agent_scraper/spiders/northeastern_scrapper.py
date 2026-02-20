import scrapy


class NortheasternScrapperSpider(scrapy.Spider):
    name = 'northeastern_scrapper'
    start_urls = ['https://northeasternmichiganboard.com/realtors.htm']
    custom_settings = {
        'FEED_URI': 'northeastern_data.csv',
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

    def parse(self, response):
        for data in response.css('table[height="5598"] tr'):
            full_name = ''
            if data.css('td[width="39%"] strong::text').get():
                full_name = data.css('td[width="39%"] strong::text').get('').strip().replace('*', '')
            else:
                if data.css('td[width="39%"] b::text').get():
                    full_name = data.css('td[width="39%"] b::text').get('').strip().replace('*', '')
            item = dict()
            item['Full Name'] = full_name
            if len(full_name.split(' ')) > 1:
                item['First Name'] = full_name.split(' ')[0].strip()
                item['Last Name'] = full_name.split(' ')[1].strip()
            if data.css('td[width="39%"] strong::text').get():
                item['Business Name'] = data.css('td[width="27%"] strong::text').get('').strip()
            else:
                if data.css('td[width="39%"] b::text').get():
                    item['Business Name'] = data.css('td[width="27%"] b::text').get('').strip()
            if data.xpath('.//td[@width="27%"]/text()').get():
                item['Street Address'] = data.xpath('.//td[@width="27%"]/text()').get().strip()
            street_address = data.xpath('.//td[@width="27%"]/br/following::br/following::text()').get('')
            if 'Voice:' not in street_address:
                street_address = data.xpath('.//td[@width="27%"]/br/following::br/following::text()').get().strip()
                state = street_address.split(',')
                if len(state) > 1:
                    item['State_Abrv'] = state[1].strip().split(' ')[0]
            else:
                item['Phone Number'] = street_address.replace('Voice: ', '').strip()
            item['Business_Site'] = data.css('td[width="27%"] a::text').get('').strip()
            item['Source_URL'] = 'www.NortheasternMichiganBoard.com'
            item['Occupation'] = 'Realtor'
            item['Lead_Source'] = 'NortheasternMichiganBoard'
            yield item

