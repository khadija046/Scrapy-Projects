import scrapy


class SmtarScrapperSpider(scrapy.Spider):
    name = 'SMTAR_scrapper'
    start_urls = ['https://members.smtar.com/realtor-directory/FindStartsWith?term=%23%21']
    base_url = 'https:{}'
    custom_settings = {
        'FEED_URI': 'SMTAR_data.csv',
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
        for data in response.css('div.gz-directory-card-body'):
            full_name = data.css('h5[itemprop="name"] a::text').get().strip()
            item = dict()
            item['Full Name'] = full_name
            if len(full_name.split(' ')) == 2:
                item['First Name'] = full_name.split(' ')[0]
                item['Last Name'] = full_name.split(' ')[1]
            else:
                if len(full_name.split(' ')) == 3:
                    item['First Name'] = full_name.split(' ')[0]
                    item['Last Name'] = full_name.split(' ')[2]
                else:
                    item['Last Name'] = full_name.split(' ')[-1]
            item['Business Name'] = data.css('span.gz-list-org-name::text').get('')
            item['Phone Number'] = data.css('span[itemprop="telephone"]::text').get('').strip()
            item['Detail_Url'] = self.base_url.format(data.css('h5[itemprop="name"] a::attr(href)').get(''))
            item['State_Abrv'] = data.css('span[itemprop="addressRegion"]::text').get('')
            item['Source_URL'] = 'www.SMTAR.com'
            item['Occupation'] = 'Realtor'
            item['Lead_Source'] = 'SMTAR'
            yield item
