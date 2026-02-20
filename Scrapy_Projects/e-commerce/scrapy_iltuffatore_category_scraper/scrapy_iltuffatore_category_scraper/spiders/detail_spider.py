import scrapy


class DetailSpiderSpider(scrapy.Spider):
    name = 'detail_spider'
    custom_settings = {
        'FEED_URI': f'output/iltuffatore_details.xlsx',
        'FEED_FORMAT': 'xlsx',
        'FEED_EXPORT_ENCODING': 'utf-8',
        'FEED_EXPORTERS': {'xlsx': 'scrapy_xlsx.XlsxItemExporter'},
    }
    start_urls = ['https://iltuffatore.es/']
    headers = {
        'authority': 'iltuffatore.es',
        'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,'
                  'application/signed-exchange;v=b3;q=0.9',
        'accept-language': 'en-US,en;q=0.9',
        'sec-ch-ua': '"Google Chrome";v="105", "Not)A;Brand";v="8", "Chromium";v="105"',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
                      'Chrome/105.0.0.0 Safari/537.36 '
    }

    def parse(self, response):
        for data in response.css('li.wide li.menu-item-object-custom a'):
            yield scrapy.Request(url=data.css('::attr(href)').get(), callback=self.parse_data, headers=self.headers)

    def parse_data(self, response):
        for data in response.css('div.top-product-section a.product-category'):
            yield scrapy.Request(url=data.css('::attr(href)').get(), callback=self.detail_page, headers=self.headers)

        next_page = response.css('a.next::attr(href)').get('')
        if next_page:
            yield scrapy.Request(url=next_page, callback=self.parse, headers=self.headers)

    def detail_page(self, response):
        yield {
            'title': response.css('h1.product_title::text').get(),
            'price': response.css('p.price bdi::text').get('').strip(),
            'isbn': response.css('span.sku::text').get(),
            'estado': response.xpath("//div[contains(@class,'short-description')]/p/b[text()='Estado: "
                                     "']/following::text()").get(),
            'product_url': response.url
        }
