import scrapy


class OlivelabsScrapperSpider(scrapy.Spider):
    name = 'olivelabs_scrapper'
    start_urls = ['https://baymard.com/ecommerce-design-examples/58-account-dashboard?showAll=true']
    base_url = 'https://baymard.com{}'

    custom_settings = {
        'FEED_URI': 'baymardss_data.csv',
        'FEED_FORMAT': 'csv',
        'FEED_EXPORT_ENCODING': 'utf-8-sig',
    }

    def parse(self, response):
        brand_id = 1
        for data in response.css('a.card'):
            brand_url = data.css('::attr(href)').get()
            if not brand_url.startswith(self.base_url):
                brand_url = self.base_url.format(brand_url)
            brand_name = data.css('p.c-lesPJm::text').get()
            date1 = data.xpath('.//div[contains(@class,"c-lesPJm-iiSSHGj-css")]/*/span/span/text()').get('')
            date2 = data.xpath('//div[contains(@class,"c-lesPJm-iiSSHGj-css")]/*/span/span/span/text()').get()
            date = date1 + '-' + date2
            pro_name = str(brand_id) + '-' + brand_name
            image_url = data.css('noscript img[data-nimg="fill"]::attr(src)').get()
            new_image = image_url.split('?')[0]
            img_url = new_image + '?w=1100&h=1669&dpr=2&auto=format&q=50'
            yield {
                'Brand_id': brand_id,
                'Brand_name': brand_name,
                'Date': date,
                'Brand_url': brand_url,
                'Product_Name_url': {pro_name.replace("'", ""): img_url},
                'Image_url': image_url
            }
            brand_id += 1

