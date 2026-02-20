import pgeocode
import scrapy
from geopy import Nominatim


class DairyqueenBarSpider(scrapy.Spider):
    name = 'dairyqueen_bar'
    start_urls = ['https://www.dairyqueen.com/en-us/locations/']
    graphapi = 'https://prod-api.dairyqueen.com/graphql/'
    # custom_settings = {
    #     'FEED_URI': 'greateruticachamberofcommerce.csv',
    #     'FEED_FORMAT': 'csv',
    #     'FEED_EXPORT_ENCODING': 'utf-8-sig',
    #     'FEED_EXPORT_FIELDS': ['Business Name', 'Full Name', 'First Name', 'Last Name', 'Street Address',
    #                            'Valid To', 'State', 'Zip', 'Description', 'Phone Number', 'Phone Number 1', 'Email',
    #                            'Business_Site', 'Social_Media', 'Record_Type',
    #                            'Category', 'Rating', 'Reviews', 'Source_URL', 'Detail_Url', 'Services',
    #                            'Latitude', 'Longitude', 'Occupation',
    #                            'Business_Type', 'Lead_Source', 'State_Abrv', 'State_TZ', 'State_Type',
    #                            'SIC_Sectors', 'SIC_Categories',
    #                            'SIC_Industries', 'NAICS_Code', 'Quick_Occupation', 'Scraped_date', 'Meta_Description']
    # }

    headers = {
        'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,'
                  'application/signed-exchange;v=b3;q=0.9',
        'accept-language': 'en-US,en;q=0.9',
        'sec-ch-ua': '"Google Chrome";v="105", "Not)A;Brand";v="8", "Chromium";v="105"',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
                      'Chrome/105.0.0.0 Safari/537.36 '
    }
    payload = {
        "operationName": "NearbyStores",
        "variables": {
            "lat": 32.944,
            "lng": -85.9539,
            "country": "US",
            "searchRadius": 25
        },
        "query": "fragment StoreDetailFields on Store {\n  id\n  storeNo\n  address3\n  city\n  stateProvince\n  postalCode\n  country\n  latitude\n  longitude\n  phone\n  conceptType\n  restaurantId\n  utcOffset\n  supportedTimeModes\n  advanceOrderDays\n  storeHours(hoursFormat: \"yyyy/MM/dd HH:mm\") {\n    calendarType\n    ranges {\n      start\n      end\n      weekday\n      __typename\n    }\n    __typename\n  }\n  minisite {\n    webLinks {\n      isDeliveryPartner\n      description\n      url\n      __typename\n    }\n    hours {\n      calendarType\n      ranges {\n        start\n        end\n        weekday\n        __typename\n      }\n      __typename\n    }\n    amenities {\n      description\n      featureId\n      __typename\n    }\n    __typename\n  }\n  flags {\n    blizzardFanClubFlag\n    brazierFlag\n    breakfastFlag\n    cakesFlag\n    canPickup\n    comingSoonFlag\n    creditCardFlag\n    curbSideFlag\n    deliveryFlag\n    driveThruFlag\n    foodAndTreatsFlag\n    giftCardsFlag\n    isAvailableFlag\n    mobileDealsFlag\n    mobileOrderingFlag\n    mtdFlag\n    ojQuenchClubFlag\n    onlineOrderingFlag\n    ojFlag\n    temporarilyClosedFlag\n    __typename\n  }\n  labels {\n    key\n    value\n    __typename\n  }\n  __typename\n}\n\nquery NearbyStores($lat: Float!, $lng: Float!, $country: String!, $searchRadius: Int!) {\n  nearbyStores(\n    lat: $lat\n    lon: $lng\n    country: $country\n    radiusMiles: $searchRadius\n    limit: 50\n    first: 20\n    order: {distance: ASC}\n  ) {\n    pageInfo {\n      endCursor\n      hasNextPage\n      __typename\n    }\n    nodes {\n      distance\n      distanceType\n      store {\n        ...StoreDetailFields\n        __typename\n      }\n      __typename\n    }\n    __typename\n  }\n}\n"
    }
    api_headers = {
        'authority': 'prod-api.dairyqueen.com',
        'accept': '*/*',
        'accept-language': 'en-us',
        'content-type': 'application/json',
        'origin': 'https://www.dairyqueen.com',
        'partner-platform': 'Web',
        'referer': 'https://www.dairyqueen.com/',
        'sec-ch-ua': '"Google Chrome";v="107", "Chromium";v="107", "Not=A?Brand";v="24"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"Windows"',
        'sec-fetch-dest': 'empty',
        'sec-fetch-mode': 'cors',
        'sec-fetch-site': 'same-site',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/107.0.0.0 Safari/537.36'
    }

    def parse(self, response):
        for data in response.css('li.Locations_location-list__rJs1U li a'):
            state = data.css('::text').get()
            state_url = data.css('::attr(href)').get()
            if state_url:
                item = dict()
                item['State'] = state
                yield response.follow(url=state_url, callback=self.parse_city, headers=self.headers, meta={'item': item})

    def parse_city(self, response):
        item = response.meta['item']
        for data in response.css('li.Locations_location-list__rJs1U li a'):
            city = data.css('::text').get()
            state = item.get('State', '')
            geo_locator = Nominatim(user_agent="geoapiExercises")
            place_1 = "{}, {}, USA"
            location = geo_locator.geocode(place_1.format(city, state))
            data_1 = location.raw
            location_data = data_1['display_name'].split()
            zipc = location_data[-3].replace(',', '')
            if zipc.isdigit():
                nomi = pgeocode.Nominatim('us')
                location = nomi.query_postal_code(zipc)
                lati = location.latitude
                print(lati)
                longi = location.longitude
                print(longi)

