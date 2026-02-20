import copy
import csv
import json
import re
from typing import Iterable

import scrapy
from nameparser import HumanName
from scrapy import Request
import datetime


class realtor(scrapy.Spider):
    name = 'realtor'
    headers = {
    'accept': '*/*',
    'accept-language': 'en-GB,en-US;q=0.9,en;q=0.8',
    'content-type': 'application/json',
    'newrelic': 'eyJ2IjpbMCwxXSwiZCI6eyJ0eSI6IkJyb3dzZXIiLCJhYyI6IjM3ODU4NCIsImFwIjoiMTM4NjIzNjUwMiIsImlkIjoiMDJlOTg0MTljNmE0NGNkMSIsInRyIjoiZjRjY2JjMmM4ZDkyZmYzZTk1OTM4OWQyYmNjOWUwNmYiLCJ0aSI6MTc1OTg0OTg1MDQyMywidGsiOiIxMDIyNjgxIn19',
    'origin': 'https://www.realtor.com',
    'priority': 'u=1, i',
    'rdc-client-name': 'agent-branding-profile',
    'rdc-client-version': '0.0.679',
    'referer': 'https://www.realtor.com/realestateagents/kaufman_tx/intent-buy',
    'sec-ch-ua': '"Google Chrome";v="141", "Not?A_Brand";v="8", "Chromium";v="141"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"Windows"',
    'sec-fetch-dest': 'empty',
    'sec-fetch-mode': 'cors',
    'sec-fetch-site': 'same-origin',
    'traceparent': '00-f4ccbc2c8d92ff3e959389d2bcc9e06f-02e98419c6a44cd1-01',
    'tracestate': '1022681@nr=0-1-378584-1386236502-02e98419c6a44cd1----1759849850423',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/141.0.0.0 Safari/537.36',
    'cookie': '__vst=035d7351-0ebd-4c51-92fa-bd68d31f16d2; __bot=false; permutive-id=19f79dcf-d068-4ba1-97ae-67a2232e3802; __split=40; G_ENABLED_IDPS=google; s_ecid=MCMID%7C15631181608799247154471373960728438712; cto_bundle=EroIEV9rV0tOcFh6dENpWWJIWGd6OU5ESk5sVG1jN3EzQmM2bEx6WGZtcWNSS1M4YmdlVWMxTDd5V0M5YXc0RWRkWDBKdzJMczJSNDFUVmpDM0RMRkNvNlc4UUlJOUVMYVAlMkJhOExaWTdRTkE2V3RTalhJSGY4QndkZ01JNTJJcmRpd2VXckhwTkVOTWpmaE5GOVloR0NyUm1qJTJCSFFHVUZrWkdGdXJFejRmU3BpMThrdHdmUnFCcGtCUllxSDQ4QVdqcjRBQkpBRGJDTU5teXJ2WnM5THVONWt5MnhwUEdWSkUwcndLRmJqb3U1TGkyS1JxT2R4VTJZVU5SJTJGSTFvZk1ZTk9yNWViaDdTZDB0dENqbWRObkhrWnF0VjFjQ0t3M2t5SEQ2SyUyRnNiVUpiV0ZsS2YzSHAlMkJ0bHI5Rmt4R25hUjZNOTY; ajs_anonymous_id=62360a03-864f-4859-bf31-b4bb5ed0ecc4; _ga=GA1.1.1141421718.1747211893; __spdt=63d6232bbc2844c3ac484445ce4b56ea; AMP_MKTG_c07a79acf5=JTdCJTdE; split_tcv=187; __rdc_id=rdc-id-1e4b31d7-b575-4aa4-8584-53946de05f65; _lr_env_src_ats=false; kampyleUserSession=1758300304194; kampyleUserSessionsCount=4; kampyleUserPercentile=61.06352317644579; _gcl_au=1.1.861951037.1758300306; _fbp=fb.1.1758300305955.3898210220; __ssn=de788ed1-b602-4d59-b2fa-76c9edcc6fae; __ssnstarttime=1759849771; split=n; AMCVS_8853394255142B6A0A4C98A4%40AdobeOrg=1; AMCV_8853394255142B6A0A4C98A4%40AdobeOrg=-1124106680%7CMCIDTS%7C20369%7CMCMID%7C15631181608799247154471373960728438712%7CMCAAMLH-1760454578%7C3%7CMCAAMB-1760454578%7CRKhpRz8krg2tLO6pguXWp5olkAcUniQYPHaMWWgdJ3xzPWQmdj0y%7CMCOPTOUT-1759856978s%7CNONE%7CMCAID%7CNONE%7CvVersion%7C5.2.0; _lr_retry_request=true; ab.storage.sessionId.7cc9d032-9d6d-44cf-a8f5-d276489af322=g%3A30cf04a3-9d8f-cc52-93ad-847d18c6cc2d%7Ce%3A1759851581389%7Cc%3A1759849781389%7Cl%3A1759849781389; ab.storage.deviceId.7cc9d032-9d6d-44cf-a8f5-d276489af322=g%3A5ee91084-b710-66a6-ef97-b60c2f44e2ef%7Ce%3Aundefined%7Cc%3A1736787394335%7Cl%3A1759849781391; ab.storage.userId.7cc9d032-9d6d-44cf-a8f5-d276489af322=g%3Avisitor_035d7351-0ebd-4c51-92fa-bd68d31f16d2%7Ce%3Aundefined%7Cc%3A1747211884206%7Cl%3A1759849781392; claritas_24hrexp_sitevisit=true; crto_is_user_optout=false; crto_mapped_user_id_NewsAndInsights=WMHvQF9HZHFpJTJCZTVEZENYa2tDalJtNUphMkFWSXYlMkZ3M1YlMkI3SkVXVEI2UUZ1VzFjJTNE; crto_mapped_user_id_ForSale=MkXHhF9HZHFpJTJCZTVEZENYa2tDalJtNUphMkJCVTFleDByVk1qdFIzMkwxMzJoTEUlM0Q; crto_mapped_user_id_Rental=cTl5zV9HZHFpJTJCZTVEZENYa2tDalJtNUphMk9IQUhYVU9yJTJCYWszVWdXaU9SS01yMCUzRA; leadid_token-27789EFE-7A9A-DB70-BB9B-97D9B7057DBB-01836014-7527-FD48-9B7F-1A40A9705CFE=B1AEF308-6242-FF3E-1F9B-5C04CED7C599; _uetsid=a9e146d0a38f11f0aad69db22019f777|wt20pu|2|fzy|0|2106; kampyleSessionPageCounter=12; AMP_c07a79acf5=JTdCJTIyZGV2aWNlSWQlMjIlM0ElMjI0ZmI3MTgyYy00YjlmLTQ3YjctOTk1OC04ZTI4NjZmNDNlYjklMjIlMkMlMjJ1c2VySWQlMjIlM0ElMjIwMzVkNzM1MS0wZWJkLTRjNTEtOTJmYS1iZDY4ZDMxZjE2ZDIlMjIlMkMlMjJzZXNzaW9uSWQlMjIlM0ExNzU5ODQ5Nzg4NTMzJTJDJTIyb3B0T3V0JTIyJTNBZmFsc2UlMkMlMjJsYXN0RXZlbnRUaW1lJTIyJTNBMTc1OTg0OTgxMzk3NCUyQyUyMmxhc3RFdmVudElkJTIyJTNBNjIlMkMlMjJwYWdlQ291bnRlciUyMiUzQTAlN0Q=; _uetvid=5c850b10d1cf11efa58aa1bd648cd65b|1n1b6l2|1759849815194|2|1|bat.bing.com/p/insights/c/z; KP_UIDz-ssn=02TbwWR91P4MxfMHZpYocjUewC9EE5vdUVXFxUtquSvejIWorgJtoLk2lCGRNlv0GlCj1ddEDncqEQmQdZSGXupDtFnglW5DxYYlpqjigLkk7kMUS3sQpKG4d2U47BdBeqWOdVcRhOnqlFLuiBm7FuT5et1SJyj4hsBP4fNk5hsIq9; KP_UIDz=02TbwWR91P4MxfMHZpYocjUewC9EE5vdUVXFxUtquSvejIWorgJtoLk2lCGRNlv0GlCj1ddEDncqEQmQdZSGXupDtFnglW5DxYYlpqjigLkk7kMUS3sQpKG4d2U47BdBeqWOdVcRhOnqlFLuiBm7FuT5et1SJyj4hsBP4fNk5hsIq9; _ga_07XBH6XBNS=GS2.1.s1759849785$o11$g1$t1759849847$j58$l0$h2134668571; _ga_MS5EHT6J6V=GS2.1.s1759849786$o11$g1$t1759849847$j59$l0$h0',
}
    json_data = {
        'operationName': 'SearchAgents',
        'variables': {
            'searchAgentInput': {
                'name': '',
                'postal_code': '',
                'languages': [],
                'agent_type': [
                    'BUYER',
                ],
                'marketing_area_city': 'mi_monroe',
                'sort': 'RELEVANT_AGENTS',
                'offset': 0,
                'agent_filter_criteria': 'NRDS_AND_FULFILLMENT_ID_EXISTS',
                'limit': 24,
            },
        },
        'query': 'query SearchAgents($searchAgentInput: SearchAgentInput) {\n  search_agents(search_agent_input: $searchAgentInput) {\n    agents {\n      id\n      is_paid\n      is_realtor\n      fulfillment_id\n      avatar {\n        url\n        initials\n        __typename\n      }\n      broker {\n        name\n        fulfillment_id\n        __typename\n      }\n      fullname\n      ratings_reviews {\n        average_rating\n        recommendations_count\n        reviews_count\n        __typename\n      }\n      listing_stats {\n        combined_annual {\n          min\n          max\n          __typename\n        }\n        for_sale {\n          count\n          last_listing_date\n          max\n          min\n          __typename\n        }\n        recently_sold_annual {\n          count\n          __typename\n        }\n        recently_sold_listing_details {\n          listings {\n            baths\n            beds\n            city\n            photo\n            state_code\n            __typename\n          }\n          show_additional\n          __typename\n        }\n        __typename\n      }\n      services {\n        buyer\n        seller\n        __typename\n      }\n      sorting_weight\n      __typename\n    }\n    matching_rows\n    __typename\n  }\n}',
    }
    url = 'https://www.realtor.com/frontdoor/graphql'
    base_url = 'https://www.realtor.com/realestateagents/{}'
    custom_settings = {
        'FEED_URI': f'output/Realtor_data_{datetime.datetime.now().strftime("%d-%m-%Y %H-%M")}.xlsx',
        'FEED_FORMAT': 'xlsx',
        'FEED_EXPORTERS': {'xlsx': 'scrapy_xlsx.XlsxItemExporter'},
        'FEED_EXPORT_ENCODING': 'utf-8',
        'FEED_EXPORT_FIELDS': ['full_name', 'first_name', 'middle_name', 'last_name',
                               'mobile_number', 'office_number', 'served_areas',
                               'street_address_1', 'street_address_2', 'city', 'state', 'zip_code',
                               'specializations', 'company_name', 'working_from', 'detail_url', 'Land Pro'],
    }

    def read_input_file(self):
        with open('input/address.csv', 'r') as csvFile:
            return list(csv.DictReader(csvFile))

    def start_requests(self) -> Iterable[Request]:
        data = self.read_input_file()
        for search in data[:]:
            county = search.get('County', '')
            state = search.get('State', '')
            query = f'{state.lower()}_{county.lower().replace(" ", "-")}'
            payload = copy.deepcopy(self.json_data)
            payload['variables']['searchAgentInput']['marketing_area_city'] = query
            yield scrapy.Request(url=self.url, headers=self.headers, body=json.dumps(payload), method='POST',
                                 meta={'query': query, 'offset': 0})

    def parse(self, response):
        json_data = json.loads(response.text)
        search_agents = json_data.get('data', {}).get('search_agents', {})
        for agent in search_agents.get('agents', []):
            item = dict()
            fullname = agent.get('fullname', '')
            name_parts = self.get_name_parts(fullname)
            item['full_name'] = name_parts.get('full_name', '')
            item['first_name'] = name_parts.get('first_name', '')
            item['middle_name'] = name_parts.get('middle_name', '')
            item['last_name'] = name_parts.get('last_name', '')
            item['company_name'] = agent.get('broker', {}).get('name', '')
            agent_id = agent.get('id', '')
            if agent_id:
                yield scrapy.Request(url=self.base_url.format(agent_id), headers=self.headers,
                                     callback=self.parse_details, meta={'item': item})

        total_records = search_agents.get('matching_rows', 0)
        current_offset = response.meta['offset']
        next_offset = current_offset + 24
        if next_offset <= int(total_records):
            payload = copy.deepcopy(self.json_data)
            query = response.meta['query']
            payload['variables']['searchAgentInput']['marketing_area_city'] = query
            payload['variables']['searchAgentInput']['offset'] = next_offset
            yield scrapy.Request(url=self.url, headers=self.headers, body=json.dumps(payload), method='POST',
                                 meta={'query': query, 'offset': next_offset})

    def parse_details(self, response):
        item = response.meta['item']
        next_data = response.css('script#__NEXT_DATA__::text').get('').strip()
        json_data = json.loads(next_data)
        agentDetailPageProps = json_data.get('props', {}).get('pageProps', {}).get('agentDetailPageProps', {}).get(
            'branding', {})
        phones = agentDetailPageProps.get('phones', [])
        if phones:
            for phone in phones:
                type_phone = phone.get('type', '')
                if 'mobile' in type_phone.lower():
                    item['mobile_number'] = phone.get('value', '')
                if 'office' in type_phone.lower():
                    item['office_number'] = phone.get('value', '')

        address = agentDetailPageProps.get('office', {}).get('address', {})
        if address:
            item['street_address_1'] = address.get('address_formatted_line_1', '')
            item['street_address_2'] = address.get('address_formatted_line_2', '')
            item['city'] = address.get('city', '')
            item['state'] = address.get('state_code', '')
            item['zip_code'] = address.get('postal_code', '')
        served_areas = agentDetailPageProps.get('served_areas', [])
        service_area = []
        if served_areas:
            for area in served_areas:
                city = area.get('name', '')
                state = area.get('state_code', '')
                clean_area = f'{city}, {state}'
                if clean_area not in service_area:
                    service_area.append(clean_area)
        item['served_areas'] = ' | '.join(areas for areas in service_area)
        specializations = agentDetailPageProps.get('specializations', [])
        specializations_list = []
        for spec in specializations:
            raw_name = spec.get('name', '')
            if raw_name not in specializations_list:
                specializations_list.append(raw_name)
        item['specializations'] = ' | '.join(spec_name for spec_name in specializations_list)
        item['website'] = agentDetailPageProps.get('website', '')
        item['working_from'] = agentDetailPageProps.get('experience', {}).get('first_year', '')
        item['detail_url'] = response.url
        found = False
        for ser in specializations_list:
            if 'Land' in ser or 'land' in ser:
                item['Land Pro'] = 'Yes'
                found = True
                break
        if not found:
            item['Land Pro'] = 'NA'
        yield item

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
