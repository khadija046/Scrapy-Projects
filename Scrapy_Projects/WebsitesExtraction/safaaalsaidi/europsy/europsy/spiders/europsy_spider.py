import scrapy


class EuropsySpiderSpider(scrapy.Spider):
    name = 'europsy_spider'
    start_urls = ['https://www.europsy.eu/search-psychologist?family_name=&language=all&op=Search&form_build_id=form'
                  '-J_7zH4RjLBj2PbFYHKWbd7Xm0WGeojrSP06RecVxiFc&form_id=psychologist_search_form']
    base_url = 'https://www.europsy.eu{}'
    custom_settings = {
        'FEED_URI': 'europsy.csv',
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

    def parse(self, response):
        for data in response.xpath('//li[@class="psychologist__list--item-bullet"]'):
            detail_url = data.xpath('./a/@href').get()
            if not detail_url.startswith(self.base_url):
                detail_url = self.base_url.format(detail_url)
            item = {'Language': data.xpath('.//td[contains(text(),"Language")]/following-sibling::td/text()').get()}
            yield scrapy.Request(url=detail_url, callback=self.parse_detail, meta={'item': item}, headers=self.headers)

        next_page = response.css('li.pager-next a::attr(href)').get()
        if next_page:
            yield response.follow(url=next_page, callback=self.parse, headers=self.headers)

    def parse_detail(self, response):
        item = response.meta['item']
        item['Name'] = response.css('h2.psychologist__name::text').get('').strip(),
        item['Gender'] = response.xpath('//td[contains(text(),"Gender")]/following-sibling::td/text()').get('').strip(),
        item['Email'] = response.xpath('//td[contains(text(),"Email")]/following-sibling::td/text()').get('').strip(),
        item['Phone Number'] = response.xpath('//td[contains(text(),"Mobile")]/following-sibling::td/text()').get('').strip(),
        item['Phone Number 1'] = response.xpath('//td[contains(text(),"Phone")]/following-sibling::td/text()').get(
            '').strip(),
        item['Detail_url'] = response.url
        yield item
