import scrapy


class GgarScrapperSpider(scrapy.Spider):
    name = 'ggar_scrapper'
    start_urls = ['https://www.ggar.com/index.php?xsearch%5B0%5D=f&xsearch%5B1%5D=&submit=Search&xsearch_id'
                  '=rets_agents_search_home&src=directory&srctype=lister&view=rets_agents']
    base_url = 'https://www.ggar.com/{}'
    custom_settings = {
        'FEED_URI': 'ggar_data.csv',
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
    headers = {
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
        'Accept-Language': 'en-US,en;q=0.9',
        'Connection': 'keep-alive',
        'Cookie': 'PHPSESSID=35mope0or6dvhhdpd4nv4u1gr7; _ga=GA1.2.193330148.1662982598; _gid=GA1.2.588892817.1662982598; __utmc=234342920; __utmz=234342920.1662982598.1.1.utmcsr=(direct)|utmccn=(direct)|utmcmd=(none); __utma=234342920.193330148.1662982598.1662982598.1662988427.2; __utmt=1; __utmb=234342920.2.10.1662988427',
        'Referer': 'https://www.ggar.com/index.php?src=directory&view=rets_agents&srctype=rets_agents_lister&query=misc7.starts.A',
        'Sec-Fetch-Dest': 'document',
        'Sec-Fetch-Mode': 'navigate',
        'Sec-Fetch-Site': 'same-origin',
        'Sec-Fetch-User': '?1',
        'Upgrade-Insecure-Requests': '1',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/105.0.0.0 Safari/537.36',
        'sec-ch-ua': '"Google Chrome";v="105", "Not)A;Brand";v="8", "Chromium";v="105"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"Windows"'
    }

    def parse(self, response):
        for data in response.xpath("//div[@class='page-fade']//p/following::p/a"):
            url = data.xpath("./@href").get()
            if not url.startswith(self.base_url):
                url = self.base_url.format(url)
            yield scrapy.Request(url=url, callback=self.parse_data, headers=self.headers)

    def parse_data(self, response):
        for data in response.css('table.retsList tr td:nth-child(1) a'):
            item = dict()
            name = data.css('::text').get().strip()
            if len(name.split(',')) > 1:
                item['First Name'] = name.split(',')[1]
                item['Last Name'] = name.split(',')[0]
            detail_url = data.css('::attr(href)').get()
            if not detail_url.startswith(self.base_url):
                detail_url = self.base_url.format(detail_url)
            item['Detail_Url'] = detail_url
            yield scrapy.Request(url=detail_url, meta={'item': item}, callback=self.detail_scrap, headers=self.headers)
        next_page = response.css('div.paginationBlankSpace a.pageLink::attr(href)').getall()
        for page in next_page:
            yield scrapy.Request(url=self.base_url.format(page),
                                 callback=self.parse_data, headers=self.headers)

    def detail_scrap(self, response):
        item = response.meta['item']
        item['Phone Number'] = response.css('span.phone::text').get('').strip()
        item['Business Name'] = response.css('a.agencyLink::text').get('').strip()
        item['Email'] = response.css('span.phone::text').get('').strip()
        item['Source_URL'] = 'www.ggar.com'
        item['Occupation'] = 'Realtor'
        item['Lead_Source'] = 'ggar'
        yield item
