import json
import urllib.parse

import scrapy


class YellowpagesSpider(scrapy.Spider):
    name = "yellowpages"
    url = "https://www.yellowpages.com/search?search_terms={}&geo_location_terms={}&page={}&s=average_rating"
    baseUrl = 'https://www.yellowpages.com{}'
    custom_settings = {
        'FEEDS': {
            'Output/yellowPages_sample.csv': {
                'format': 'csv',
                'overwrite': True,
                'encoding': 'utf-8',
            },
        }
        ,
        "DOWNLOAD_HANDLERS": {
            "http": "scrapy_zyte_api.ScrapyZyteAPIDownloadHandler",
            "https": "scrapy_zyte_api.ScrapyZyteAPIDownloadHandler",
        },
        "DOWNLOADER_MIDDLEWARES": {
            "scrapy_poet.InjectionMiddleware": 543,  # You can adjust the priority number as needed
            "scrapy_zyte_api.ScrapyZyteAPIDownloaderMiddleware": 1000
        },
        "REQUEST_FINGERPRINTER_CLASS": "scrapy_zyte_api.ScrapyZyteAPIRequestFingerprinter",
        "TWISTED_REACTOR": "twisted.internet.asyncioreactor.AsyncioSelectorReactor",
        "ZYTE_API_KEY": "212bea34868f45398d450cfd11e0a1f8",  # Please enter your API Key here
        "ZYTE_API_TRANSPARENT_MODE": True}

    locations = ['Dallas, TX']
    keywords = ["cosmetology", "cosmetologist", "hair stylist", "hairdresser"]

    headers = {
        'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
        'accept-language': 'en-GB,en-US;q=0.9,en;q=0.8',
        'priority': 'u=0, i',
        'referer': 'https://www.yellowpages.com/search?search_terms=cosmetologist&geo_location_terms=Dallas%2C+TX',
        'sec-ch-ua': '"Not)A;Brand";v="8", "Chromium";v="138", "Google Chrome";v="138"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"Windows"',
        'sec-fetch-dest': 'document',
        'sec-fetch-mode': 'navigate',
        'sec-fetch-site': 'same-origin',
        'upgrade-insecure-requests': '1',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/138.0.0.0 Safari/537.36',
        'cookie': 'vrid=7fc4d3b3-44ea-4de5-a883-b652d75aeffe; bucket=ypu%3Aypu%3Adefault; bucketsrc=default; s_otb=false; dns_l=true; __cf_bm=tMLGn4RoAni5fDlYcb0KBcvFEOj.R7Rm7rDoZTrSWM0-1753181799-1.0.1.1-rw7fy95h5TAx21R8cqGJboRoL96OS9VJFLaRQCjagip0etvXvqFIMYN1u0L6nGPVHrT7YRXJyHmklWCMpfrHHPCqqfMiK56xl69scFw1X.w; zone=300; _ga=GA1.1.2117029480.1753181804; s_fid=59AC4EBC01977199-3060D9A732CEBA0B; s_cc=true; cf_clearance=YweUxEDlb77HTTcVx56pcXPgHtIfAKATHnsXNbwasq8-1753181806-1.2.1.1-X1nWYUGFEG26LGkoSFtQAifsjHjCSOqtryTMuoiTc6_jm5L0jSLqVPGzq5kL5QFhFNmqm00SWDBdUTXXUg5O1jN7ZojtxL7fOtcvQ110CI480gPxlG3F9GXmgfLfHjuO2A4OwY_4X2irxSvnac9FYnR3nDA6XoO.uVdS5gm.p.IuDNDZXYedpT2fjCNGwA7yc1VW.Xfajjl8AYKFb1rlGvVjUFYjwjax.n_r_cq2S8U; s_vi=[CS]v1|343FB737DA42A927-4000063103DF5D08[CE]; s_prop70=July; s_prop71=30; location=geo_term%3ADallas%2C%20TX%7Clat%3A32.783333%7Clng%3A-96.8%7Ccity%3ADallas%7Cstate%3ATX%7Cdisplay_geo%3ADallas%2C%20TX; search_terms=cosmetologist; express:sess=eyJka3MiOiJiOGY5NDI0My0xNjdlLTRjZWEtOTUwOC1jYjFiYzU5MmEzOWIiLCJmbGFzaCI6e30sInByZXZpb3VzUGFnZSI6InNycCJ9; express:sess.sig=gJutCFJVwi3tIlNipD68JGwZMYg; _ga_0EQTJQH34W=GS2.1.s1753181804$o1$g1$t1753181836$j28$l0$h0; s_prop49=search_results; sorted=false; __gsas=ID=0528ebc04a84979e:T=1753181839:RT=1753181839:S=ALNI_MZRtw85fEiyhHFqhyy-fHt6SwwHPA; __gads=ID=e85867925cb97c62:T=1753181839:RT=1753181839:S=ALNI_Mb4goB3wfkNoNGQIDK6sFHgPQogfQ; __gpi=UID=000010ecc6e6e14e:T=1753181839:RT=1753181839:S=ALNI_Ma_XXRYlPmDO1HCd7_w1CF_FpY6bQ; __eoi=ID=52dbb7f9ef47d4fd:T=1753181839:RT=1753181839:S=AA-Afja6k5t7TB7Cn-cwKzlRfErM; s_tp=10144; s_nr=1753181854764; s_sq=%5B%5BB%5D%5D; s_ppv=search%2C86%2C86%2C8699',
    }

    def start_requests(self):
        for loc in self.locations[:]:
            for key in self.keywords[:]:
                raw_url = self.url.format(key, loc, '1')
                # proxy_url = self.get_proxy_url(raw_url)
                yield scrapy.Request(url= raw_url,
                                     meta={'location': loc, 'keyword': key}, headers=self.headers)

    def parse(self, response):
        jsonData = response.xpath('//script[contains(text(),"LocalBusiness")]/text()').get('').strip()
        jsonLoaded = json.loads(jsonData)
        loc = response.meta['location']
        key = response.meta['keyword']
        for Business in jsonLoaded:
            item = dict()
            item['SearchLocation'] = loc
            item['SearchKeyword'] = key
            item['Url'] = Business.get('url', '').strip()
            item['Featured'] = 'No'
            item['BusinessName'] = Business.get('name', '').strip()
            item['PhoneNumber'] = Business.get('telephone', '').strip()
            item['streetAddress'] = Business.get('address', {}).get('streetAddress', '').strip()
            item['addressLocality'] = Business.get('address', {}).get('addressLocality', '').strip()
            item['addressRegion'] = Business.get('address', {}).get('addressRegion', '').strip()
            item['postalCode'] = Business.get('address', {}).get('postalCode', '').strip()
            item['addressCountry'] = Business.get('address', {}).get('addressCountry', '').strip()
            yield scrapy.Request(url=item['Url'], callback=self.parse_details,
                                     meta={'item': item, 'featured': 'no', 'loc': loc}, headers=self.headers)

        featured = response.css('section.featured-listings div h2 a::attr(href)').getall()
        if featured:
            for featureUrl in featured:
                item = dict()
                item['SearchLocation'] = loc
                item['SearchKeyword'] = key
                # proxy_url = self.get_proxy_url()
                yield scrapy.Request(url=self.baseUrl.format(featureUrl), callback=self.parse_details,
                                     meta={'item': item, 'featured': 'yes', 'loc': loc}, headers=self.headers)

        next_page = response.css('li a.next::attr(href)').get('')
        if next_page:
            url = self.baseUrl.format(next_page)
            # proxy_urls = self.get_proxy_url(url)
            yield scrapy.Request(url=url, meta={'location': loc, 'keyword': key},
                                 callback=self.parse,headers=self.headers)

    def parse_details(self, response):
        featured = response.meta['featured']
        item = response.meta['item']
        coordinateJson = response.xpath('//script[contains(text(), "GeoCoordinates")]/text()').get('').strip()
        loadedCoordinate = json.loads(coordinateJson)
        if 'yes' in featured:
            item['Url'] = response.url
            item['Featured'] = 'Yes'
            item['BusinessName'] = loadedCoordinate.get('name', '').strip()
            item['PhoneNumber'] = loadedCoordinate.get('telephone', '').strip()
            item['streetAddress'] = loadedCoordinate.get('address', {}).get('streetAddress', '').strip()
            item['addressLocality'] = loadedCoordinate.get('address', {}).get('addressLocality', '').strip()
            item['addressRegion'] = loadedCoordinate.get('address', {}).get('addressRegion', '').strip()
            item['postalCode'] = loadedCoordinate.get('address', {}).get('postalCode', '').strip()
            item['addressCountry'] = loadedCoordinate.get('address', {}).get('addressCountry', '').strip()
        jsonText = response.xpath('//script[contains(text(),"UserLoggedIn")]/text()').get('').strip()
        json_Data = jsonText.split('YPU            = ')[-1].rsplit(';', 1)[0].strip()
        jsonLoaded = json.loads(json_Data)
        item['taCount'] = jsonLoaded.get('tripAdvisor', {}).get('ReviewCount', '')
        item['taRating'] = jsonLoaded.get('tripAdvisor', {}).get('Rating', '')
        item['WebsiteURL'] = jsonLoaded.get('listing', {}).get('websiteUrl', '')
        item['OpenHours'] = jsonLoaded.get('listing', {}).get('openWeekHours', '')
        trip_url = jsonLoaded.get('tripAdvisor', {}).get('ReviewsUrl', '')
        tripID = trip_url.split('-Reviews')[0].rsplit('-', 1)[-1].strip()
        item['tripAdvisorID'] = tripID
        item['Categories'] = ' > '.join(name.get('name', '') for name in jsonLoaded.get('listing', []).get('categories', {}))
        item['PrimaryCategory'] = jsonLoaded.get('listing', {}).get('primaryCategory', '')
        item['Email'] = jsonLoaded.get('listing', {}).get('email', '')
        item['Images'] = ', '.join(image.css('::attr(src)').get('') for image in response.css('div.carousel '
                                                                                              'a.media-thumbnail img'))
        item['PriceRange'] = loadedCoordinate.get('priceRange', '')
        item['Latitude'] = loadedCoordinate.get('geo', {}).get('latitude', '')
        item['Longitude'] = loadedCoordinate.get('geo', {}).get('longitude', '')
        item['paymentAccepted'] = loadedCoordinate.get('paymentAccepted', '')
        item['generalInfo'] = response.css('dd.general-info::text').get('').strip()
        item['socialLinks'] = ' | '.join(link.css('::attr(href)').get() for link in response.css('dd.social-links a'))
        item['Good For Family'] = response.xpath('//p[strong[contains(text(),"Good For Family")]]/text()').get('').replace(':&nbsp;', '').strip()
        item['Good for Kid'] = response.xpath('//p[strong[contains(text(),"Good for Kid")]]/text()').get('').replace(':&nbsp;', '').strip()
        item['yearInBusiness'] = response.css('div.years-in-business div strong::text').get('').strip()
        item['Amenities'] = response.xpath('//div[@class="amenities-info"]/span/text()').get('').strip()
        loc = response.meta['loc']
        yield item


