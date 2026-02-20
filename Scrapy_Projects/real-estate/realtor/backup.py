import re
import csv
import json
import scrapy
import datetime

from nameparser import HumanName


class realtor(scrapy.Spider):
    name = 'realtor'
    url = "https://www.realtor.com/realestateagents/{}/pg-{}"
    first_request = "https://www.realtor.com/realestateagents/{}"
    prefix = 'https://www.realtor.com'
    headers = {
    'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
    'accept-language': 'en-GB,en-US;q=0.9,en;q=0.8',
    'cache-control': 'max-age=0',
    'priority': 'u=0, i',
    'referer': 'https://www.realtor.com/',
    'sec-ch-ua': '"Chromium";v="140", "Not=A?Brand";v="24", "Google Chrome";v="140"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"Windows"',
    'sec-fetch-dest': 'document',
    'sec-fetch-mode': 'navigate',
    'sec-fetch-site': 'same-origin',
    'sec-fetch-user': '?1',
    'upgrade-insecure-requests': '1',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/140.0.0.0 Safari/537.36',
    'cookie': '__vst=035d7351-0ebd-4c51-92fa-bd68d31f16d2; __bot=false; permutive-id=19f79dcf-d068-4ba1-97ae-67a2232e3802; __split=40; G_ENABLED_IDPS=google; s_ecid=MCMID%7C15631181608799247154471373960728438712; cto_bundle=EroIEV9rV0tOcFh6dENpWWJIWGd6OU5ESk5sVG1jN3EzQmM2bEx6WGZtcWNSS1M4YmdlVWMxTDd5V0M5YXc0RWRkWDBKdzJMczJSNDFUVmpDM0RMRkNvNlc4UUlJOUVMYVAlMkJhOExaWTdRTkE2V3RTalhJSGY4QndkZ01JNTJJcmRpd2VXckhwTkVOTWpmaE5GOVloR0NyUm1qJTJCSFFHVUZrWkdGdXJFejRmU3BpMThrdHdmUnFCcGtCUllxSDQ4QVdqcjRBQkpBRGJDTU5teXJ2WnM5THVONWt5MnhwUEdWSkUwcndLRmJqb3U1TGkyS1JxT2R4VTJZVU5SJTJGSTFvZk1ZTk9yNWViaDdTZDB0dENqbWRObkhrWnF0VjFjQ0t3M2t5SEQ2SyUyRnNiVUpiV0ZsS2YzSHAlMkJ0bHI5Rmt4R25hUjZNOTY; ajs_anonymous_id=62360a03-864f-4859-bf31-b4bb5ed0ecc4; _ga=GA1.1.1141421718.1747211893; __spdt=63d6232bbc2844c3ac484445ce4b56ea; AMP_MKTG_c07a79acf5=JTdCJTdE; split_tcv=187; __ssn=f9b58f0b-0bb1-4ad6-95b5-de22044e748f; __ssnstarttime=1758300298; __rdc_id=rdc-id-1e4b31d7-b575-4aa4-8584-53946de05f65; split=n; _lr_retry_request=true; _lr_env_src_ats=false; AMCVS_8853394255142B6A0A4C98A4%40AdobeOrg=1; AMCV_8853394255142B6A0A4C98A4%40AdobeOrg=-1124106680%7CMCIDTS%7C20351%7CMCMID%7C15631181608799247154471373960728438712%7CMCAAMLH-1758905101%7C3%7CMCAAMB-1758905101%7CRKhpRz8krg2tLO6pguXWp5olkAcUniQYPHaMWWgdJ3xzPWQmdj0y%7CMCOPTOUT-1758307501s%7CNONE%7CMCAID%7CNONE%7CvVersion%7C5.2.0; ab.storage.sessionId.7cc9d032-9d6d-44cf-a8f5-d276489af322=g%3Aaef9a60c-04a7-1b2c-857c-785ee66722cf%7Ce%3A1758302102766%7Cc%3A1758300302767%7Cl%3A1758300302767; ab.storage.deviceId.7cc9d032-9d6d-44cf-a8f5-d276489af322=g%3A5ee91084-b710-66a6-ef97-b60c2f44e2ef%7Ce%3Aundefined%7Cc%3A1736787394335%7Cl%3A1758300302768; ab.storage.userId.7cc9d032-9d6d-44cf-a8f5-d276489af322=g%3Avisitor_035d7351-0ebd-4c51-92fa-bd68d31f16d2%7Ce%3Aundefined%7Cc%3A1747211884206%7Cl%3A1758300302769; kampyleUserSession=1758300304194; kampyleUserSessionsCount=4; kampyleUserPercentile=61.06352317644579; _gcl_au=1.1.861951037.1758300306; _fbp=fb.1.1758300305955.3898210220; claritas_24hrexp_sitevisit=true; leadid_token-27789EFE-7A9A-DB70-BB9B-97D9B7057DBB-01836014-7527-FD48-9B7F-1A40A9705CFE=33C2847B-4DE7-968D-A65A-591D983897FE; crto_is_user_optout=false; crto_mapped_user_id_NewsAndInsights=RXhm419HZHFpJTJCZTVEZENYa2tDalJtNUphMkNwdnQxdlpSTEZidCUyRktYd1k5YUc5WSUzRA; crto_mapped_user_id_ForSale=2TDY1l9HZHFpJTJCZTVEZENYa2tDalJtNUphMk1LWFRpQmRoZkZrTGxsNGUlMkY1V3hhNCUzRA; crto_mapped_user_id_Rental=Q4ZV719HZHFpJTJCZTVEZENYa2tDalJtNUphMkFnR1RxS1hnb2lnQWxOc0h6N25zT28lM0Q; KP_UIDz-ssn=02QhgsGIlE1qvR6k2AdQZh0619s94JgiGa3EWoSOULDpi50jYEf9eLa5r4CRQz3ieqpizCmntY6Gt0I7GTMS9lcZs06fP0WHT6oID11SwVVqago7xs5wYoa0nzmsCH3rYBVQMXhXkEmjtRssQJU5X9DnQSLDhbM5Q90qP2PditZP4k; KP_UIDz=02QhgsGIlE1qvR6k2AdQZh0619s94JgiGa3EWoSOULDpi50jYEf9eLa5r4CRQz3ieqpizCmntY6Gt0I7GTMS9lcZs06fP0WHT6oID11SwVVqago7xs5wYoa0nzmsCH3rYBVQMXhXkEmjtRssQJU5X9DnQSLDhbM5Q90qP2PditZP4k; AMP_c07a79acf5=JTdCJTIyZGV2aWNlSWQlMjIlM0ElMjI0ZmI3MTgyYy00YjlmLTQ3YjctOTk1OC04ZTI4NjZmNDNlYjklMjIlMkMlMjJ1c2VySWQlMjIlM0ElMjIwMzVkNzM1MS0wZWJkLTRjNTEtOTJmYS1iZDY4ZDMxZjE2ZDIlMjIlMkMlMjJzZXNzaW9uSWQlMjIlM0ExNzU4MzAwMzA3NDg0JTJDJTIyb3B0T3V0JTIyJTNBZmFsc2UlMkMlMjJsYXN0RXZlbnRUaW1lJTIyJTNBMTc1ODMwMDM4OTMxOSUyQyUyMmxhc3RFdmVudElkJTIyJTNBNDclMkMlMjJwYWdlQ291bnRlciUyMiUzQTAlN0Q=; _uetsid=ffffb2e0957711f0afebc7849c6be65a|ibbt5n|2|fzg|0|2088; _uetvid=5c850b10d1cf11efa58aa1bd648cd65b|19y5z4f|1758300390427|4|1|bat.bing.com/p/insights/c/a; kampyleSessionPageCounter=6; _ga_MS5EHT6J6V=GS2.1.s1758300307$o9$g1$t1758300405$j38$l0$h0; _ga_07XBH6XBNS=GS2.1.s1758300307$o9$g1$t1758300405$j38$l0$h487011008',
}

    custom_settings = {
        'FEED_URI': f'output/Realtor_data_{datetime.datetime.now().strftime("%d-%m-%Y %H-%M")}.xlsx',
        'FEED_FORMAT': 'xlsx',
        'FEED_EXPORTERS': {'xlsx': 'scrapy_xlsx.XlsxItemExporter'},
        'FEED_EXPORT_ENCODING': 'utf-8',
        'FEED_EXPORT_FIELDS': ['title', 'role', 'full_name', 'first_name', 'last_name',
                                'mobile_number', 'office_number', 'served_areas',
                                'street_address_1', 'street_address_2', 'city', 'state', 'zip_code',
                                'specializations', 'company_name', 'working_from', 'detail_url', 'Land Pro'],
        }

    def read_input_file(self):
        with open('input/address.csv', 'r') as csvFile:
            return list(csv.DictReader(csvFile))

    def start_requests(self):

        data = self.read_input_file()
        for search in data[:1]:
            county = search.get('County', '')
            state = search.get('State', '')
            query = f'{county.lower().replace(" ", "-")}_{state.lower()}'
            page , offset = 1, 0
            yield scrapy.Request(self.first_request.format(query), callback=self.parse, headers=self.headers,
                                 meta={'search': search, 'offset': offset, 'current': page})

    def parse(self, response):
        offset = response.meta['offset']
        page_no = response.meta['current']
        search = response.meta['search']
        county = search.get('County', '')
        state = search.get('State', '')
        query = f'{county.lower().replace(" ", "-")}_{state.lower()}'
        try:
            script_data = response.xpath('//script[@id="__NEXT_DATA__"]/text()').get('').strip()
            print(script_data)
            json_loaded = json.loads(script_data)
            agents = json_loaded.get('props', {}).get('pageProps', {}).get('agentSearchResultsPageProps', {})
            for agent in agents.get('agents', []):
                item = dict()
                item['title'] = agent.get('title', '')
                item['role'] = agent.get('role', '').title()
                first_name = agent.get('first_name', '')
                if not first_name:
                    full_name = self.get_name_parts(agent.get('person_name', '').strip())
                    item['full_name'] = full_name.get('full_name', '')
                    item['first_name'] = full_name.get('first_name', '')
                    item['last_name'] = full_name.get('last_name', '')
                else:
                    item['full_name'] = agent.get('person_name', '')
                    item['first_name'] = agent.get('first_name', '')
                    item['last_name'] = agent.get('last_name', '')
                phones = agent.get('phones', [])
                if phones:
                    for phone in phones:
                        type_phone = phone.get('type', '')
                        if 'Mobile' in type_phone:
                            item['mobile_number'] = phone.get('number', '')
                        if 'Office' in type_phone:
                            item['office_number'] = phone.get('number', '')
                served_areas = agent.get('served_areas', [])
                service_area = []
                if served_areas:
                    for area in served_areas:
                        city = area.get('name', '')
                        state = area.get('state_code', '')
                        clean_area = f'{city}, {state}'
                        if clean_area not in service_area:
                            service_area.append(clean_area)
                item['served_areas'] = ' | '.join(areas for areas in service_area)
                address = agent.get('address', {})
                if address:
                    item['street_address_1'] = address.get('line', '')
                    item['street_address_2'] = address.get('line2', '')
                    item['city'] = address.get('city', '')
                    item['state'] = address.get('state_code', '')
                    item['zip_code'] = address.get('postal_code', '')
                else:
                    item['street_address_1'] = ''
                    item['street_address_2'] = ''
                    item['city'] = ''
                    item['state'] = ''
                    item['zip_code'] = ''
                specializations = agent.get('specializations', [])
                specializations_list = []
                for spec in specializations:
                    raw_name = spec.get('name', '')
                    if raw_name not in specializations_list:
                        specializations_list.append(raw_name)
                if specializations:
                    item['specializations'] = ' | '.join(spec_name for spec_name in specializations_list)
                item['company_name'] = agent.get('broker', {}).get('name', '')
                item['website'] = agent.get('href', '')
                item['working_from'] = agent.get('first_year', '')
                item['detail_url'] = agent.get('web_url', '')
                found = False
                for ser in specializations_list:
                    if 'Land' in ser or 'land' in ser:
                        item['Land Pro'] = 'Yes'
                        found = True
                        break
                if not found:
                    item['Land Pro'] = 'NA'
                yield item
            total_data = agents.get('matching_rows', '')
            next_offset = offset + 20
            if next_offset <= int(total_data):
                next_page = page_no + 1
                print(f'Next Page is: {next_page}')
                if next_page:
                    yield scrapy.Request(self.url.format(query, str(next_page)), callback=self.parse,
                                         headers=self.headers,dont_filter=True,
                                         meta={'search': search, 'offset': next_offset, 'current': next_page})
        except Exception as ex:
            print(ex)

    def get_name_parts(self, name):
        name_parts = HumanName(name)
        punctuation_re = re.compile(r'[^\w-]')
        return {
            'full_name': name.strip(),
            'prefix': re.sub(punctuation_re, '', name_parts.title),
            'first_name': re.sub(punctuation_re, '', name_parts.first),
            'middle_name': re.sub(punctuation_re, '', name_parts.middle),
            'last_name': re.sub(punctuation_re, '', name_parts.last),
            'suffix': re.sub(punctuation_re, '', name_parts.suffix)
    }


