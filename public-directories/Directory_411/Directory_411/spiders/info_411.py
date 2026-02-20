import csv
import math
from datetime import datetime
from typing import Iterable

import scrapy
from scrapy import Request


class Info411Spider(scrapy.Spider):
    name = "info_411"
    url = "https://411.info/search/?q={}&l={}&page={}"
    base_url = 'https://411.info{}'
    custom_settings = {
        'FEED_URI': f'outputs/411_directory_{datetime.now().strftime("%d-%m-%Y %H-%M")}.csv',
        'FEED_FORMAT': 'csv',
        'FEED_EXPORT_ENCODING': 'utf-8',
    }
    headers = {
        'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
        'accept-language': 'en-GB,en-US;q=0.9,en;q=0.8',
        'priority': 'u=0, i',
        'referer': 'https://411.info/search?q=advisor&l=Tampa%2C+FL',
        'sec-ch-ua': '"Google Chrome";v="135", "Not-A.Brand";v="8", "Chromium";v="135"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"Windows"',
        'sec-fetch-dest': 'document',
        'sec-fetch-mode': 'navigate',
        'sec-fetch-site': 'same-origin',
        'sec-fetch-user': '?1',
        'upgrade-insecure-requests': '1',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/135.0.0.0 Safari/537.36',
        'Cookie': 'PHPSESSID=gnf59pl8e4lm85m7mujdmutkv6; _411=eyJsciI6ImVuLXVzIiwicHQiOiJiIn0%3D; _ga=GA1.1.2031532300.1745597219; __gsas=ID=2b6cfef2484382c3:T=1745597219:RT=1745597219:S=ALNI_MYjo2Bl9YLoo0lfVkMXIAIxEaq3Iw; __gads=ID=741cfb93b422e322:T=1745597218:RT=1745695624:S=ALNI_Mb4qc9EuVmdTpqDiW1VSuH6Fp0DDg; __gpi=UID=00001098bb1f1ef4:T=1745597218:RT=1745695624:S=ALNI_MYfVD0DyScMUWDJ-xnJow9_PrmhLQ; __eoi=ID=209d81da2d04902a:T=1745597218:RT=1745695624:S=AA-AfjbGMASbwf_DeCQzqB2lX_ec; FCNEC=%5B%5B%22AKsRol9TfS-SiNsXkP5h9e4PcfygA8DBc8fOW1IfHK6EYV0la1WhjejLJTkosOT3k0xr4DLDft2MNFKi9AfY-1WZWT4cHfYUxCmguGX9Yl03e5PkktjsroTvWbsgvIB4M5j76KeqVPFC3volXfXXpIAuO5X0-dIoCg%3D%3D%22%5D%5D; _ga_T2X6VXPSMT=GS1.1.1745695624.3.0.1745695630.54.0.0; _411=eyJsciI6ImVuLXVzIiwicHQiOiJiIn0%3D'
    }

    def read_csv(self, filename):
        with open(filename, 'r') as csvFile:
            return list(csv.DictReader(csvFile))

    def start_requests(self) -> Iterable[Request]:
        professions = self.read_csv('input/professions.csv')
        locations = self.read_csv('input/locations.csv')
        for profess in professions:
            search_advisor = profess.get('keyword', '').strip()
            for loc_area in locations:
                location = loc_area.get('location', '').strip()
                loc_query = location.replace(' ', '+').replace(',', '%2C')
                yield scrapy.Request(url=self.url.format(search_advisor, loc_query, 1),
                                     headers=self.headers, meta={'search': search_advisor, 'location': loc_query,
                                                             'current_page': 1})

    def parse(self, response):
        search_key = response.meta['search']
        location = response.meta['location']
        current_page = response.meta['current_page']
        print(f'Currently Processing: Page No {current_page}...')
        for data in response.xpath('//div[contains(@class,"listings")]/div[contains(@class,"list_")]/a[div]'):
            item = dict()
            detail = data.xpath('./@href').get('').strip()
            if not detail.startswith('https://411.info'):
                detail = self.base_url.format(detail)
            item['Searched Profession'] = search_key
            item['Searched Location'] = location.replace('+', ' ').replace('%2C', ',')
            item['Detail Url'] = detail
            item['Name'] = data.css('div[itemprop="name"]::text').get('').strip()
            item['Phone Number'] = data.css('div[itemprop="telephone"]::text').get('').strip()
            item['Street Address'] = data.css('span[itemprop="streetAddress"]::text').get('').strip()
            item['City'] = data.css('span[itemprop="addressLocality"]::text').get('').strip()
            item['State'] = data.css('span[itemprop="addressRegion"]::attr(title)').get('').strip() or data.css('abbr[itemprop="addressRegion"]::attr(title)').get('').strip()
            item['State_abbr'] = data.css('span[itemprop="addressRegion"]::text').get('').strip() or data.css('abbr[itemprop="addressRegion"]::text').get('').strip()
            item['Zip Code'] = data.css('span[itemprop="postalCode"]::text').get('').strip()
            yield item

        total_records = response.xpath('//ul[@class="breadcrumb"]/li/strong/text()').get('0').strip()
        total_pages = math.ceil(int(total_records)/30)
        next_page = current_page + 1
        if next_page <= total_pages:
            yield scrapy.Request(url=self.url.format(search_key, location, next_page),
                                 headers=self.headers, meta={'search': search_key, 'location': location,
                                                             'current_page': next_page})

