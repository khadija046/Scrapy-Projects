import scrapy


class HeinzeSpiderSpider(scrapy.Spider):
    name = 'heinze_spider'
    start_urls = ['https://www.heinze.de/expertenprofile-zu/?s=1&p=1&d=c&ft=1&cn=EU&cy=DE&gs=11&sf=T1717T14935869']
    custom_settings = {
        'FEED_URI': 'heinze.csv',
        'FEED_FORMAT': 'csv',
        'FEED_EXPORT_ENCODING': 'utf-8-sig',
        'FEED_EXPORT_FIELDS': ['Rank', 'Quelle / Link zum Kontakt', 'Büro', 'Strasse', 'PLZ',
                               'Stadt', 'Detail_url', 'Personen', 'Anrede', 'Tel', 'Mail']
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
        item = {'Rank': 0}
        yield scrapy.Request(url=self.start_urls[0], callback=self.parse, headers=self.headers, meta={'item': item})

    def parse(self, response):
        item = response.meta['item']
        record_no = item.get('Rank')
        for data in response.css('div.cardText a.cssHeadline'):
            detail_url = data.css('::attr(href)').get()
            record_no += 1
            new_rank = {'Rank': record_no}
            if detail_url:
                yield response.follow(url=detail_url, callback=self.parse_company_details,
                                      headers=self.headers, meta={'item': new_rank})

        next_page = response.css('li.pagination-next a::attr(href)').get()
        if next_page:
            item['Rank'] = record_no
            yield response.follow(url=next_page, callback=self.parse, headers=self.headers, meta={'item': item})

    def parse_company_details(self, response):
        rank = response.meta['item']
        if response.css('div.cardText'):
            for data in response.css('div.cardText'):
                item = dict()
                item['Rank'] = rank.get('Rank')
                item['Quelle / Link zum Kontakt'] = response.css('a[itemprop="url"]::attr(href)').get('').strip()
                item['Büro'] = response.css('p[itemprop="legalName"]::text').get('').strip()
                item['Strasse'] = response.css('p[itemprop="streetAddress"]::text').get('').strip()
                item['PLZ'] = response.css('span[itemprop="postalCode"]::text').get('').strip()
                item['Stadt'] = response.css('span[itemprop="addressLocality"]::text').get('').strip()
                if data.css('a.cssHeadline::text'):
                    item['Personen'] = data.css('a.cssHeadline::text').get('').strip()
                    profile_url = data.css('a.cssHeadline::attr(href)').get()
                    yield response.follow(url=profile_url, callback=self.team_member_detail,
                                          headers=self.headers, meta={'item': item})
                else:
                    if data.css('p.cssHeadline::text'):
                        item['Personen'] = data.css('p.cssHeadline::text').get('').strip()
                        item['Anrede'] = ''
                        item['Tel'] = ''
                        item['Mail'] = ''
                        yield item
                    else:
                        item['Personen'] = ''
                        item['Anrede'] = ''
                        item['Tel'] = ''
                        item['Mail'] = ''
                        yield item
        else:
            item = dict()
            item['Rank'] = rank.get('Rank')
            item['Quelle / Link zum Kontakt'] = response.css('a[itemprop="url"]::attr(href)').get('').strip()
            item['Büro'] = response.css('p[itemprop="legalName"]::text').get('').strip()
            item['Strasse'] = response.css('p[itemprop="streetAddress"]::text').get('').strip()
            item['PLZ'] = response.css('span[itemprop="postalCode"]::text').get('').strip()
            item['Stadt'] = response.css('span[itemprop="addressLocality"]::text').get('').strip()
            item['Tel'] = response.css('a[itemprop="telephone"]::attr(href)').get('').replace('tel:', '').strip()
            item['Mail'] = ''
            item['Personen'] = ''
            item['Anrede'] = ''
            item['Detail_url'] = response.url
            yield item

    def team_member_detail(self, response):
        item = response.meta['item']
        item['Anrede'] = response.css('div.cssPersonName p.cssH4::text').get('').strip()
        item['Tel'] = response.css('div.cssASideContact a.cssBlack::attr(href)').get('').replace('tel:', '').strip()
        item['Mail'] = response.xpath('//a[contains(text(), "@")]/text()').get('').strip()
        yield item
