import scrapy


class TallpinesrealtorsScrapperSpider(scrapy.Spider):
    name = 'tallpinesrealtors_scrapper'
    start_urls = ['https://tallpinesrealtors.com/about-us/member-directory/']
    custom_settings = {
        'FEED_URI': 'tallpinesrealtors_data.csv',
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
        for data in response.css('div.member'):
            item = dict()
            full_name = data.css('div.member-personnel ul:nth-child(2) li::text').get('').strip()
            if len(full_name.split(' ')) > 1:
                item['First Name'] = full_name.split(' ')[0]
                item['Last Name'] = full_name.split(' ')[1]
            item['Full Name'] = full_name
            item['Business Name'] = data.css('h5.member-name::text').get()
            item['Street Address'] = data.css('.member-street::text').get()
            state_address = data.css('.member-csz::text').get('').strip().split(' ')
            if len(state_address) > 1:
                if len(state_address) > 3:
                    item['State_Abrv'] = state_address[2]
                    item['Zip'] = state_address[3]
                else:
                    item['State_Abrv'] = state_address[1]
                    item['Zip'] = state_address[2]
            item['Phone Number'] = data.xpath(
                './/div[@class="member-phone"]/span/following-sibling::text()').get(' ').strip()
            item['Source_URL'] = 'tallpinesrealtors.com'
            item['Occupation'] = 'Realtor'
            item['Lead_Source'] = 'tallpinesrealtors'
            yield item
