import codecs
import csv
import requests
from bs4 import BeautifulSoup
from lxml import etree


def read_csv():
    try:
        with codecs.open('redfin.csv', 'r', encoding="utf-8", errors='ignore') as reader:
            return list(csv.DictReader(reader))
    except Exception as ex:
        print('Error while Reading File | ' + str(ex))


def write_csv(write_values):
    try:
        print('Wait Inserting Values to CSV')
        keys = write_values[0].keys()
        with open('output/redfin.csv', 'w', newline='') as csvfile:
            dict_writer = csv.DictWriter(csvfile, keys)
            dict_writer.writeheader()
            dict_writer.writerows(write_values)
        print('Inserted!!!')
    except Exception as ex:
        print('Error while Writing Values to CSV | ' + str(ex))


def get_values():
    request_urls = read_csv()
    headers = {
        'authority': 'www.redfin.com',
        'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
        'accept-language': 'en-GB,en-US;q=0.9,en;q=0.8',
        'cache-control': 'max-age=0',
        # Requests sorts cookies= alphabetically
        # 'cookie': '_schn=_sfe35eh; _scid=a76c9581-df8b-48a7-84bc-07afab9548f7; _sctr=1|1669402800000; RF_CORVAIR_LAST_VERSION=446.0.1; RF_BROWSER_ID=eA6Rc3TISPqiYc0vAr2TeA; RF_BID_UPDATED=1; RF_MARKET=houston; RF_BUSINESS_MARKET=22; _gcl_au=1.1.1208637070.1669385723; ki_r=; __pdst=fd08f8e88538456481a0d7bce47c4ae4; ln_or=d; _rdt_uuid=1669385726389.07354e43-eaa0-4cf5-9051-b00dfc7da388; _tt_enable_cookie=1; _ttp=2ebce0a2-8b9c-45cd-bec3-ea2b8108d9be; _gid=GA1.2.810100967.1669385727; RF_BROWSER_CAPABILITIES=%7B%22screen-size%22%3A4%2C%22events-touch%22%3Afalse%2C%22ios-app-store%22%3Afalse%2C%22google-play-store%22%3Afalse%2C%22ios-web-view%22%3Afalse%2C%22android-web-view%22%3Afalse%7D; _pin_unauth=dWlkPU16UTBabU0xT0RZdFpHUmlaUzAwT1RJM0xXSXdaR0V0TVdGaE5EZGlPR1ZoWkdGbQ; userPreferences=parcels%3Dtrue%26schools%3Dfalse%26mapStyle%3Ds%26statistics%3Dtrue%26agcTooltip%3Dfalse%26agentReset%3Dfalse%26ldpRegister%3Dfalse%26afCard%3D2%26schoolType%3D0%26lastSeenLdp%3DnoSharedSearchCookie; G_ENABLED_IDPS=google; __gads=ID=e60c6601565fa516:T=1669385862:S=ALNI_MaVkPW6ULQ83BU1ZvJeifE0ODcb7A; __gpi=UID=00000b263376c74c:T=1669385862:RT=1669385862:S=ALNI_MZN7nyJDyUIV_uanlsjEhUtemyu0A; AKA_A2=A; run_fs_for_user=336; ak_bmsc=821B7E80AD1489D6343A6B8564028045~000000000000000000000000000000~YAAQPmswF9AVYpaEAQAA4EOMshHF5hrilJImvmYPIyjOSS+Agb9P4zzJMCfZFpU3M5Q02VbopHfbXIIl79YLMUMZyd0l/Gb2EIM3BfmlV39h/keggv8Ta6GFUH8/ktSYFNPF3n5C1HRjcOhImOUohinkDMz+Fjro3RDjeTOBNW+VAC7Ftinal6dnmzyd72wRqKd0AXX/bdFmEYqU1BzUrv5LOUJcDzdyElLCzHkpHA7jvfpx+/RPiVnoURX+PzfIwS/AaQ1J90m417T20tpNSW5RHhJiaEU62nkLE9d4l2ytVL5YYEn859TeNAgniFo8Gh97/75nLFID1PrISoilPxzubLEGTtfzgqohoAnipCl/5omFHonP8Qy7WApSp0B+MR8yDs0iiH2QAp1rbZrO7vWEj6XBNgZ2nzXMloZDo5QcwKhUyjkcacVwCSIGTBndZstMZuXVw841nKZuY8k6mHydJmq8U1JT1i778duNt3N2Y8/KznmtceY=; RF_LDP_VIEWS_FOR_PROMPT=%7B%22viewsData%22%3A%7B%2211-25-2022%22%3A%7B%22161266672%22%3A1%2C%22161711616%22%3A1%2C%22162211492%22%3A1%2C%22162570635%22%3A1%7D%2C%2211-26-2022%22%3A%7B%22162779863%22%3A1%7D%7D%2C%22expiration%22%3A%222024-11-24T14%3A15%3A28.730Z%22%2C%22totalPromptedLdps%22%3A0%7D; PageCount=1; RF_LISTING_VIEWS=162779863.161266672.161711616.162211492.162570635; RF_LAST_DP_SERVICE_REGION=3358; _uetsid=9bd948706ccb11ed9b96ab8f960a63c1; _uetvid=f5fe92203ef211ed86648b975295c8e8; _ga_HTE8FN6558=GS1.1.1669442857.2.0.1669442857.0.0.0; AMP_TOKEN=%24NOT_FOUND; _ga=GA1.2.350720181.1669385725; ki_t=1669385723952%3B1669442863900%3B1669442863900%3B2%3B7; cto_bundle=32wNMV83Uk5mdDVJZmhhSjRFVGRkNHlDeWtkNXBVT1F1OE5hRkpOVktncWZobmZvNHFlTmhGWWRrQlNpYW5uOXVhbEQxMll0MCUyRnkyWmZlTnJGZ3VjUlcwcjNKTzBRRUprJTJGRUs2RDdKNDRBTUdKdENVRG51c2k1aVhnUDA5cTNwN1NBazBDVFAxUDF4Q2xJRVNYN0Z3T3lFb2pRJTNEJTNE; _ga_928P0PZ00X=GS1.1.1669442856.2.1.1669442886.30.0.0; RF_VISITED=true; bm_sv=5C0E804FDEDDA914B45C5E7F3C11399C~YAAQPmswF0EZYpaEAQAA8g6NshET4ntBxeqwsBeBMb9EytqBetYQ6+2rDuWpw5W8FXEnHz3XF6E2vick7VJlo1ejzLTW0wyaSH/eLVbCBCppmyOvhiqGfdJ+oTk67cYXap8WtSr8+gba62jG8XWhkzRZOp/RBZmr3gYWLdplBVqJ2wu7yC11TiPVGx7RK1kH0jVGZ5H16Kv3NGVrY7PHbwMnByXN7uG8ibRlgQGLFQ6V0KbYhH8kNdRVbhf1ct9mBg==~1',
        'sec-ch-ua': '"Google Chrome";v="107", "Chromium";v="107", "Not=A?Brand";v="24"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"Windows"',
        'sec-fetch-dest': 'document',
        'sec-fetch-mode': 'navigate',
        'sec-fetch-site': 'same-origin',
        'sec-fetch-user': '?1',
        'upgrade-insecure-requests': '1',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/107.0.0.0 Safari/537.36',
    }
    get_data = []
    print('Getting Values !!!! \n\n')
    for url in request_urls:
        try:
            item = dict()
            item['URL'] = url.get('URL')
            item['LATITUDE'] = url.get('LATITUDE')
            item['LONGITUDE'] = url.get('LONGITUDE')
            htmlpage = requests.get(url.get('URL'), headers=headers)
            soup = BeautifulSoup(htmlpage.content, "html.parser")
            dom = etree.HTML(str(soup))
            est_value = dom.xpath('//span[contains(text(),"Est. Mo. Payment")]/following-sibling::span')
            if est_value:
                item['Est. Mo. Payment'] = est_value[0].text
            else:
                item['Est. Mo. Payment'] = 'NaN'
            rental_value = dom.xpath('//div[@id="rentalEstimate-collapsible"]/div[2]/div/p')
            if rental_value:
                item['Rental Estimate'] = rental_value[0].text
            else:
                item['Rental Estimate'] = 'NaN'
            get_data.append(item)
        except Exception as ex:
            print('Error while getting values | ' + str(ex))
            continue
    write_csv(get_data)


if __name__ == '__main__':
    get_values()
