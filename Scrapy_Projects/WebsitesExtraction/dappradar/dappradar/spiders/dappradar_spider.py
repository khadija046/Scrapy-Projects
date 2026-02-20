import json

import scrapy


class DappradarSpiderSpider(scrapy.Spider):
    name = 'dappradar_spider'
    request_api = 'https://dappradar.com/v2/api/dapps?params=UkdGd2NGSmhaR0Z5Y0dGblpUMDBKbk5uY205MWNEMXRZWGdtWTNWeWNtVnVZM2s5VlZORUptaHBaR1V0WVdseVpISnZjSE05TUNabVpXRjBkWEpsWkQweEpuSmhibWRsUFdSaGVTWndjbTkwYjJOdmJEMWxkR2hsY21WMWJTWnpiM0owUFhWelpYSW1iM0prWlhJOVpHVnpZeVpzYVcxcGREMHlOZz09'
    headers = {
        'authority': 'dappradar.com',
        'accept': 'application/json, text/plain, */*',
        'accept-language': 'en-GB,en-US;q=0.9,en;q=0.8',
        # 'cookie': '__cf_bm=.HB_1JRVvoz_VzfvZB5n.4EBA.J1IbfzE2JFoh.cXok-1666771352-0-AacWtkj3GfouPPPeUGhxN9i1Dsy7wmF0VNR7u5y3MZzpvfaaXIjzNnx16miINKqDRBjFXNxSvNaHvCqqIQ+zLBg=; _omappvp=VtFdhxDbIRxDoXK0sFUX1Y1HVPM2C1ZciKnPE4JGjTVDSErNnCQ69MrFJFBZ0XVmRCC3GHdLHe5ONJ7gMG0ZrIBPWJdUyMVs; notification-session-identifier=f12bb85a-2c4e-4bb5-9431-c7cd68796e95; _gid=GA1.2.1879704339.1666771356; _gat=1; _cs_c=1; _rdt_uuid=1666771358017.4074b6af-1372-40c8-9049-d60acdfa6eac; _omappvs=1666771388951; _ga=GA1.1.1904420019.1666771356; omSeen-yu7339blcxy0t7u057j4=1666771395518; _ga_7R16E5X6VC=GS1.1.1666771358.1.1.1666771403.0.0.0; _cs_id=a18525a8-5d48-a538-ae61-3412504ad761.1666771357.1.1666771409.1666771357.1.1700935357957; _cs_s=4.0.1.1666773209260; cook-sec-dr=crgbncls7bim4F1TO9hXbYmhKjTRprXVk3pK1nj9lH1eLQWY56PVHOZp5P4SZ; test-cook=1; __cf_bm=icmsYdJNy8q3Zz6KENVyabgOuZ_Z9wG7rUGK4kAYQZ4-1666771702-0-AYG+OTFEy+lxrEmsXPf6N0FRcmrSNXZBFfxRb155RmNhO9CBwryeBjjxETrCuIcnJ+fO1cOUUuAdpIrmeXM53aY=',
        'referer': 'https://dappradar.com/rankings/protocol/ethereum/2',
        'sec-ch-ua': '"Chromium";v="106", "Google Chrome";v="106", "Not;A=Brand";v="99"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"Windows"',
        'sec-fetch-dest': 'empty',
        'sec-fetch-mode': 'cors',
        'sec-fetch-site': 'same-origin',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/106.0.0.0 Safari/537.36'
    }
    def start_requests(self):
        yield scrapy.Request(url=self.request_api, callback=self.parse, headers=self.headers)

    def parse(self, response):
        result = json.loads(response.body)
        print(result)
