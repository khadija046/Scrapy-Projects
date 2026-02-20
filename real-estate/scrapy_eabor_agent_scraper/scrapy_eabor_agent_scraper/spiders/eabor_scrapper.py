import scrapy


class EaborScrapperSpider(scrapy.Spider):
    name = 'eabor_scrapper'
    start_urls = ['https://members.eabor.org/directory/FindStartsWith?term=%23%21']
    base_url = 'https:{}'

    custom_settings = {
        'FEED_URI': 'eabor_data.csv',
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
            full_name = data.css('h5[itemprop="name"] a::text').get('').strip()
            item = dict()
            if len(full_name.split(' ')) <= 3:
                full_name = full_name
                if len(full_name.split(' ')) > 1:
                    item['First Name'] = full_name.split(' ')[0]
                    if len(full_name.split(' ')) == 3:
                        item['Last Name'] = full_name.split(' ')[2]
                    else:
                        item['Last Name'] = full_name.split(' ')[1]
            else:
                full_name = ''
            detail_url = data.css('h5 a::attr(href)').get()
            if not detail_url.startswith(self.base_url):
                detail_url = self.base_url.format(detail_url)
            if full_name:
                item['Full Name'] = full_name
                item['Business Name'] = data.css('span.gz-list-org-name::text').get('').strip()
                item['Phone Number'] = data.css('span[itemprop="telephone"]::text').get('').strip()
                item['Street Address'] = data.css('span[itemprop="streetAddress"]::text').get('').strip()
                item['State_Abrv'] = data.css('span[itemprop="addressRegion"]::text').get('').strip()
                item['Zip'] = data.css('span[itemprop="postalCode"]::text').get('').strip()
                item['Business_Site'] = data.css('li.gz-card-website a::attr(href)').get()
                item['Detail_Url'] = detail_url
                item['Source_URL'] = 'https://www.eabor.org'
                item['Occupation'] = 'Realtor'
                item['Lead_Source'] = 'eabor'
                yield item


