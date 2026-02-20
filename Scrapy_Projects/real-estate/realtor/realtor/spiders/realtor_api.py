import copy
import csv
import json
import re
from typing import Iterable

import scrapy
from nameparser import HumanName
from scrapy import Request
import datetime


class RealtorApiSpider(scrapy.Spider):
    name = "realtor_api"
    headers = {
    'accept': '*/*',
    'accept-language': 'en-US,en;q=0.9',
    'content-type': 'application/json',
    'newrelic': 'eyJ2IjpbMCwxXSwiZCI6eyJ0eSI6IkJyb3dzZXIiLCJhYyI6IjM3ODU4NCIsImFwIjoiMTM4NjIzNjUwMiIsImlkIjoiZWI5OTEyNWM5OTQ3ODQ4NyIsInRyIjoiODA4YjNjZDBmNDM2OWRkN2YxMDE4NjFlZDM2NjVkNzMiLCJ0aSI6MTc2ODAzNzUzNzI5NywidGsiOiIxMDIyNjgxIn19',
    'origin': 'https://www.realtor.com',
    'priority': 'u=1, i',
    'rdc-client-name': 'agent-branding-profile',
    'rdc-client-version': '0.0.701',
    'referer': 'https://www.realtor.com/realestateagents/kaufman_tx/intent-buy',
    'sec-ch-ua': '"Google Chrome";v="143", "Chromium";v="143", "Not A(Brand";v="24"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"Windows"',
    'sec-fetch-dest': 'empty',
    'sec-fetch-mode': 'cors',
    'sec-fetch-site': 'same-origin',
    'traceparent': '00-808b3cd0f4369dd7f101861ed3665d73-eb99125c99478487-01',
    'tracestate': '1022681@nr=0-1-378584-1386236502-eb99125c99478487----1768037537297',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/143.0.0.0 Safari/537.36',
    'cookie': 'split_tcv=154; __ssn=b1847fe6-ca05-49a9-972b-d441ce1fcc0b; __ssnstarttime=1768035635; __vst=7d3628db-47b7-45fa-ab6a-259754cdb16d; __bot=false; isAuth0GnavEnabled=C; __rdc_id=rdc-id-d2daeb6d-fd58-45bf-b3b9-1e09b3a0bb01; _lr_retry_request=true; _lr_env_src_ats=false; ab.storage.deviceId.7cc9d032-9d6d-44cf-a8f5-d276489af322=g%3Ac3cf978c-c416-32bd-06b1-3c021f1983bb%7Ce%3Aundefined%7Cc%3A1747749662880%7Cl%3A1768035638437; ab.storage.userId.7cc9d032-9d6d-44cf-a8f5-d276489af322=g%3Avisitor_7d3628db-47b7-45fa-ab6a-259754cdb16d%7Ce%3Aundefined%7Cc%3A1768035638434%7Cl%3A1768035638437; __split=86; split=n; pbjs-unifiedid=%7B%22TDID%22%3A%22488412b1-980f-4bc4-b390-f3be89dff970%22%2C%22TDID_LOOKUP%22%3A%22TRUE%22%2C%22TDID_CREATED_AT%22%3A%222025-12-10T09%3A00%3A37%22%7D; pbjs-unifiedid_cst=zix7LPQsHA%3D%3D; AMCVS_8853394255142B6A0A4C98A4%40AdobeOrg=1; _gcl_au=1.1.1052516481.1768035639; _fbp=fb.1.1768035639460.3699539028; claritas_24hrexp_sitevisit=true; panoramaId_expiry=1768640438392; _cc_id=3fe1ba3042206efca2cd4b445a917880; panoramaId=a0e41916f268f4d687c7d7fafab416d5393894871ede30ab4a3c29cfd5394cf3; G_ENABLED_IDPS=google; permutive-id=d41c6e95-108a-43cf-afed-7c6affc2a957; s_ecid=MCMID%7C64990388384128528610934559531555113476; AMCV_8853394255142B6A0A4C98A4%40AdobeOrg=-1124106680%7CMCIDTS%7C20464%7CMCMID%7C64990388384128528610934559531555113476%7CMCAAMLH-1768640439%7C3%7CMCAAMB-1768640439%7CRKhpRz8krg2tLO6pguXWp5olkAcUniQYPHaMWWgdJ3xzPWQmdj0y%7CMCOPTOUT-1768042839s%7CNONE%7CMCAID%7CNONE%7CvVersion%7C5.2.0; _ga=GA1.1.1571708693.1768035640; __spdt=9fd147013f5a448eb651239af60c425e; ajs_anonymous_id=873ee6fa-020e-40f7-8dd7-7fed0e9ed5b6; analytics_session_id=1768035640572; rdc_last_touch_marketing_channel={%22ltmc%22:%22organic%20search%22%2C%22detail%22:%22www.google.com%22%2C%22ttl%22:%222026-02-09T09:00:40.576Z%22}; __gads=ID=ade0f4dd1bf8b4e6:T=1768035639:RT=1768035639:S=ALNI_MYoiRziqRn5XsktnXdCumTwwp6yYg; __gpi=UID=000012e93ac2f91c:T=1768035639:RT=1768035639:S=ALNI_MbRefj8c8iOdsTlBQPEEoRBYMY4Cg; __eoi=ID=f76a6c315ec64407:T=1768035639:RT=1768035639:S=AA-AfjaqlQBgFnGlRUFEE-1jJy04; crto_is_user_optout=false; crto_mapped_user_id_Rental=eKqFRF9ZR0FXVXJlTzlzSEl2eEtyZ2VxY21qbTdsS3VhUGV5QmZtZEJBVFc5SGV3JTNE; crto_mapped_user_id_NewsAndInsights=1_Sy1F9ZR0FXVXJlTzlzSEl2eEtyZ2VxY21oMEQlMkYlMkZsT3dHTWczYzNxT0Z4ajF0QSUzRA; crto_mapped_user_id_ForSale=C8jyul9ZR0FXVXJlTzlzSEl2eEtyZ2VxY21zS0F4UGZUWVd4NUdDWGRrWmw1VEVrJTNE; ndp_session_id=b18aeaa6-91eb-4f73-b8c4-12400968e4ea; AMP_MKTG_c07a79acf5=JTdCJTIycmVmZXJyZXIlMjIlM0ElMjJodHRwcyUzQSUyRiUyRnd3dy5nb29nbGUuY29tJTJGJTIyJTJDJTIycmVmZXJyaW5nX2RvbWFpbiUyMiUzQSUyMnd3dy5nb29nbGUuY29tJTIyJTdE; AMP_c07a79acf5=JTdCJTIyZGV2aWNlSWQlMjIlM0ElMjIxYTczMjE0Zi1kYjk1LTQ0OTAtYTIzYS05MTcxZDk3NzY1YTklMjIlMkMlMjJ1c2VySWQlMjIlM0ElMjI3ZDM2MjhkYi00N2I3LTQ1ZmEtYWI2YS0yNTk3NTRjZGIxNmQlMjIlMkMlMjJzZXNzaW9uSWQlMjIlM0ExNzY4MDM1NjQwOTk2JTJDJTIyb3B0T3V0JTIyJTNBZmFsc2UlMkMlMjJsYXN0RXZlbnRUaW1lJTIyJTNBMTc2ODAzNTY0MTAwNyUyQyUyMmxhc3RFdmVudElkJTIyJTNBMyUyQyUyMnBhZ2VDb3VudGVyJTIyJTNBMCU3RA==; ab.storage.sessionId.7cc9d032-9d6d-44cf-a8f5-d276489af322=g%3A3ba49385-02bd-5663-265c-f83e18f96c78%7Ce%3A1768037442927%7Cc%3A1768035638436%7Cl%3A1768035642927; _lr_sampling_rate=100; kampyleUserSession=1768035643293; kampyleUserSessionsCount=3; kampyleUserPercentile=13.709097132606896; cto_bundle=-xxQXF9PWk9RMlUlMkZDclZPV0xBdlFpQ3pRbGE1THJHc29BNE56NmVtJTJGZ0g4NktZR2JIaTNFeFolMkZqMHljS0ZhYVlyN3RzcWZVR1V4VHN1TGljNFgyYngyb0NjNWNzQnQlMkZjdkglMkJUSTVOdnZLJTJCT2ExbGtVUnJGViUyQk5QViUyRlFMQzlQRWxMJTJGeGVXeHBYcnpobHpNeTBYMFpYTExNMHclM0QlM0Q; _awl=2.1768035643.5-bafd1a814a6dc3d64adc5ca8b5e93269-6763652d6575726f70652d7765737431-0; leadid_token-27789EFE-7A9A-DB70-BB9B-97D9B7057DBB-01836014-7527-FD48-9B7F-1A40A9705CFE=1D1B0382-3B12-CBEF-57B8-0AA9D277EFB0; kampyleInvitePresented=true; DECLINED_DATE=1768037070632; KP_UIDz-ssn=02WGfrb8vsQYynJxMSi0cOnr06geg2ud1QqC4Pd5NaKcQajXW5LUO74wyLwUYg5LJ49mrnyptMY9pwsGxHwuvQmd3ah18ALNpobyyueV2zc8KOgaD5UW33iXG6j0p1ayTO2IPscACpZaQOWpZ1IWRcm0vGobkXLSsvsl7SUlMx4d3f; KP_UIDz=02WGfrb8vsQYynJxMSi0cOnr06geg2ud1QqC4Pd5NaKcQajXW5LUO74wyLwUYg5LJ49mrnyptMY9pwsGxHwuvQmd3ah18ALNpobyyueV2zc8KOgaD5UW33iXG6j0p1ayTO2IPscACpZaQOWpZ1IWRcm0vGobkXLSsvsl7SUlMx4d3f; _uetsid=d6a8f0a0ee0211f09ab56977441c4781|1mnu9jy|2|g2l|0|2201; _uetvid=e5702320358211f097742d077d6bedd5|mjz8kq|1768037526250|7|1|bat.bing.com/p/insights/c/a; kampyleSessionPageCounter=5; kampylePageLoadedTimestamp=1768037526571; g_state={"i_l":0,"i_ll":1768037526691,"i_b":"BfVxEBBJBSKy3KgsYPCfixmJDstvKG14qKf8A8UwV2I","i_e":{"enable_itp_optimization":0}}; _ga_07XBH6XBNS=GS2.1.s1768035640$o1$g1$t1768037527$j20$l0$h922262831; _ga_MS5EHT6J6V=GS2.1.s1768035640$o1$g1$t1768037527$j20$l0$h0; analytics_session_id.last_access=1768037527795',
}
    zyteapi_proxy = 'http://5adf95f22b1a42dcb37ee5d1c806f4d7:@api.zyte.com:8011'
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
            'marketing_area_city': 'tx_kaufman',
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
        'HTTPERROR_ALLOW_ALL': True,
    }

    detail_api_payload = {
        'operationName': 'AgentBrandingProfile',
        'variables': {
            'agentBrandingInput': {
                'profile_id': '56cae3880fa417010077141f',
                'fulfillment_id': None,
                'nrds_id': None,
            },
        },
        'query': 'query AgentBrandingProfile($agentBrandingInput: AgentBrandingInput) {\n  agent_branding(agent_branding_input: $agentBrandingInput) {\n    branding {\n      fulfillment_id\n      id\n      is_paid\n      is_realtor\n      designations\n      is_realtor\n      avatar {\n        initials\n        url\n        __typename\n      }\n      bio\n      fullname\n      website\n      intent_type\n      broker {\n        name\n        website\n        fulfillment_id\n        __typename\n      }\n      languages\n      specializations {\n        name\n        __typename\n      }\n      experience {\n        first_year\n        first_month\n        label\n        __typename\n      }\n      ratings_reviews {\n        average_rating\n        reviews_count\n        recommendations_count\n        __typename\n      }\n      served_areas {\n        name\n        state_code\n        __typename\n      }\n      listing_stats {\n        combined_annual {\n          max\n          min\n          __typename\n        }\n        for_sale {\n          count\n          last_listing_date\n          min\n          max\n          __typename\n        }\n        recently_sold {\n          count\n          last_sold_date\n          min\n          max\n          __typename\n        }\n        recently_sold_annual {\n          count\n          __typename\n        }\n        recently_sold_listing_details {\n          listings {\n            baths\n            beds\n            city\n            photo\n            state_code\n            __typename\n          }\n          show_additional\n          __typename\n        }\n        __typename\n      }\n      mls {\n        mls_set\n        agent_id\n        id\n        primary\n        license_number\n        inactivation_date\n        status\n        __typename\n      }\n      office {\n        name\n        phones {\n          type\n          value\n          __typename\n        }\n        website\n        address {\n          address_formatted_line_1\n          address_formatted_line_2\n          city\n          postal_code\n          state_code\n          __typename\n        }\n        __typename\n      }\n      phones {\n        type\n        value\n        __typename\n      }\n      website\n      license_number\n      license_state\n      is_empty_profile\n      social_media {\n        facebook {\n          href\n          __typename\n        }\n        instagram {\n          href\n          __typename\n        }\n        linkedin {\n          href\n          __typename\n        }\n        tiktok {\n          href\n          __typename\n        }\n        x {\n          href\n          __typename\n        }\n        youtube {\n          href\n          __typename\n        }\n        __typename\n      }\n      about_video {\n        id\n        source\n        url\n        __typename\n      }\n      services {\n        buyer\n        seller\n        __typename\n      }\n      questions_and_answers {\n        question_text\n        answer_text\n        __typename\n      }\n      __typename\n    }\n    __typename\n  }\n}',
    }
    detail_api = 'https://www.realtor.com/frontdoor/graphql'

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
            yield scrapy.Request(url=self.url, body=json.dumps(payload), method='POST',
                                 meta={'query': query, 'offset': 0}, headers=self.headers)

    def parse(self, response):
        # print(response.text)
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
            print(item)
            agent_id = agent.get('id', '')
            if agent_id:
                payload = copy.deepcopy(self.detail_api_payload)
                payload['variables']['agentBrandingInput']['profile_id'] = agent_id
                yield scrapy.Request(url=self.detail_api,
                                     callback=self.parse_details,
                                     meta={'item': item, 'proxy': self.zyteapi_proxy},
                                     headers=self.headers,
                                     method='POST',
                                     body=json.dumps(payload))


        total_records = search_agents.get('matching_rows', 0)
        current_offset = response.meta['offset']
        next_offset = current_offset + 24
        if next_offset <= int(total_records):
            payload = copy.deepcopy(self.json_data)
            query = response.meta['query']
            payload['variables']['searchAgentInput']['marketing_area_city'] = query
            payload['variables']['searchAgentInput']['offset'] = next_offset
            yield scrapy.Request(url=self.url, body=json.dumps(payload),
                                 method='POST',
                                 meta={'query': query, 'offset': next_offset , 'proxy': self.zyteapi_proxy},
                                 headers=self.headers)


    def parse_details(self, response):
        item = response.meta['item']
        # next_data = response.css('script#__NEXT_DATA__::text').get('').strip()
        json_data = json.loads(response.text)
        agentDetailPageProps = json_data.get('data', {}).get('agent_branding', {}).get('branding', {})
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
