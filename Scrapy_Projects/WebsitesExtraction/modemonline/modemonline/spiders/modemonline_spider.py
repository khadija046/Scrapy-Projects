import scrapy


class ModemonlineSpiderSpider(scrapy.Spider):
    name = 'modemonline_spider'
    start_urls = ['https://www.modemonline.com/design/design-connections/designers',
                  'https://www.modemonline.com/fashion/mini-web-sites/fashion-schools',
                  'https://www.modemonline.com/fashion/mini-web-sites/fashion-brands',
                  'https://www.modemonline.com/art/art-connections/editors-and-media',
                  'https://www.modemonline.com/fashion/sales-campaigns/brands/spring-summer-2023',
                  'https://www.modemonline.com/design/design-connections/design-schools',
                  'https://www.modemonline.com/fashion/mini-web-sites/editors-and-media']
    custom_settings = {
        'FEED_URI': 'modemonline_new.csv',
        'FEED_FORMAT': 'csv',
        'FEED_EXPORT_ENCODING': 'utf-8-sig',
    }
    headers = {
        'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,'
                  'application/signed-exchange;v=b3;q=0.9',
        'accept-language': 'en-US,en;q=0.9',
        'sec-ch-ua': '"Google Chrome";v="105", "Not)A;Brand";v="8", "Chromium";v="105"',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
                      'Chrome/105.0.0.0 Safari/537.36 '
    }

    def start_requests(self):
        for url in self.start_urls:
            yield scrapy.Request(url=url, callback=self.parse, headers=self.headers)

    def parse(self, response):
        if response.css('div.index-brands-wrap span a'):
            for data in response.css('div.index-brands-wrap span a'):
                detail_url = data.css('::attr(href)').get()
                if detail_url:
                    yield response.follow(url=detail_url, callback=self.parse_detail, headers=self.headers)
        else:
            if response.css('div.index-tag table.content-table tr'):
                for data in response.css('div.index-tag table.content-table tr'):
                    yield {
                        'Name': data.css('td:nth-child(1)::text').get('').replace('\n', '').strip(),
                        'Address': data.css('td:nth-child(2)::text').get('').replace('\n', '').strip(),
                        'Phone': data.xpath('.//a[contains(@href, "tel")]/@href').get('').replace('tel:', '').strip(),
                        'Email': data.xpath('.//a[contains(@href, "mailto")]/@href').get('').replace('mailto:', '').strip(),
                        'Website': data.xpath('.//a[@target="_blank"]/@href').get('').strip(),
                        'Url': response.url
                    }

    def parse_detail(self, response):
        address = ''.join(response.css(
            'div.summary-content-table div.col-md-4:nth-child(3) div.ct-box:nth-child(1) div.ct-box-right::text').getall())
        yield {
            'Name': response.css('div.project-title h1::text').get('').strip(),
            'Address': address.replace('\n', '').strip(),
            'Phone': response.xpath('//a[contains(@href, "tel")]/@href').get('').replace('tel:', '').strip(),
            'Email': response.xpath('//a[contains(@href, "mailto")]/@href').get('').replace('mailto:', '').strip(),
            'Website': response.xpath('//div[@class="ct-box-right"]/a[contains(@href, "http")]/@href').get('').strip(),
            'Url': response.url
        }
