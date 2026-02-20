import csv
import json
import re

import scrapy


class RedfinAgentsSpider(scrapy.Spider):
    name = "redfin_agents"
    url = "https://www.redfin.com/stingray/do/autocomplete/agent?location={}&start=0&count=10&v=2&al=1&iss=false&ooa=true&mrs=false&region_id=NaN&region_type=NaN&lat&lng&includeAddressInfo=false&lastSearches"
    headers = {
        'sec-ch-ua-platform': '"Windows"',
        'Referer': 'https://www.redfin.com/real-estate-agents',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/137.0.0.0 Safari/537.36',
        'sec-ch-ua': '"Google Chrome";v="137", "Chromium";v="137", "Not/A)Brand";v="24"',
        'sec-ch-ua-mobile': '?0',
        'Cookie': 'RF_BID_UPDATED=1; RF_BROWSER_ID=GspOLJH3TrqHIL8Tl2DZ_w; RF_BROWSER_ID_GREAT_FIRST_VISIT_TIMESTAMP=2025-06-24T04%3A57%3A27.548220'
    }
    base_url = 'https://www.redfin.com{}'
    custom_settings = {
        'FEED_URI': f'outputs/redfin_data_sample_1.csv',
        'FEED_FORMAT': 'csv',
        'FEED_EXPORT_ENCODING': 'utf-8',
        'HTTPERROR_ALLOWED_CODES': [404]
    }
    agents = 'https://www.redfin.com/real-estate-agents/{}'

    def read_csv(self):
        with open('input/counties.csv', 'r') as csvFile:
            return list(csv.DictReader(csvFile))

    def start_requests(self):
        request_area = self.read_csv()
        for area in request_area[:]:
            zipcode = area.get('zipCode', '')
            query = f"{zipcode}"
            raw_url = self.url.format(query)
            yield scrapy.Request(url=raw_url, headers=self.headers)

    def parse(self, response):
        json_data = json.loads(response.text.replace('{}&&', ''))
        exactMatch = json_data.get('payload', {}).get('exactMatch', {})
        if exactMatch:
            location_url = exactMatch.get('url', '')
        else:
            if json_data.get('payload', {}).get('sections', []):
                section = json_data.get('payload', {}).get('sections', [])[0].get('rows', [])[0]
                location_url = section.get('url', '')
            else:
                location_url = ''
        if location_url:
            yield scrapy.Request(url=self.base_url.format(location_url), headers=self.headers, callback=self.parse_agents)

    def parse_agents(self, response):
        string_email = response.xpath('//script[contains(text(), "__reactServerState")]/text()').get('').replace('\\"',
                                                                                                                 '"').strip()
        matches = re.findall(r'"slug"\s*:\s*"([^"]+)"\s*,\s*"photoUrl"', string_email)
        for agent in matches:
            agentUrl = self.agents.format(agent)
            if agentUrl:
                yield scrapy.Request(url=agentUrl, headers=self.headers, callback=self.parse_agent)


    def parse_agent(self, response):
        item = dict()
        item['agentName'] = response.css('div[data-rf-test-name="agent-name"] h1::text').get('').strip()
        item['companyName'] = response.css('div.brokerage-name::text').get('').strip()
        item['dealsClosed'] = response.css('div.deals span.deals-amount::text').get('').strip()
        item['phoneNumber'] = response.css('a[data-rf-test-name="phone-number"]::text').get('').strip()
        item['neighborhoods'] = ', '.join(response.css('div.neighborhoods span.neighborhoods-links span a::text').getall()).strip() or response.css('div.expandable-neighborhoods span.visible::text').get('').replace('·', ',').strip()
        item['serviceBadge'] = response.css('div.service-badge div.jobTitle::text').get('').strip()
        teamAgent = []
        for team in response.css('div.PartnerTeamAgentCard, div.teammate-v2'):
            teams = dict()
            if team.css('div.agent-name'):
                teams['image'] = team.css('div.agent-photo img::attr(src)').get('').strip()
                teams['name'] = team.css('div.agent-name p::text').get('').strip()
                teams['agentLicense'] = team.css('div.agent-license p::text').get('').replace('Agent License #:',
                                                                                              '').strip()
            else:
                teams['image'] = team.css('img::attr(src)').get('').strip()
                teams['name'] = team.css('div.name::text').get('').strip()
                teams['agentJob'] = team.css('div.job::text').get('').strip()
            teamAgent.append(teams)
        item['teamAgents'] = teamAgent
        string_email = response.xpath('//script[contains(text(), "__reactServerState")]/text()').get('').replace('\\"', '"').strip()
        matches = re.findall(r'"agentEmail"\s*:\s*"([^"]+)"\s*,\s*"numHomesClosed"', string_email)
        if matches:
            last_email = matches[-1]
            item['agentEmail'] = last_email
        else:
            item['agentEmail'] = ''
        item['agentUrl'] = response.url
        yield item
