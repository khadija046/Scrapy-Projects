import json
from copy import deepcopy

import scrapy
from scrapy.utils.response import open_in_browser


class EarlyyearsSpiderSpider(scrapy.Spider):
    name = 'earlyyears_spider'''
    start_urls = ['']
    headers = {
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
        'Accept-Language': 'en-GB,en-US;q=0.9,en;q=0.8',
        'Cache-Control': 'max-age=0',
        'Connection': 'keep-alive',
        # Requests sorts cookies= alphabetically
        'Cookie': 'oam.Flash.RENDERMAP.TOKEN=-15f2o8r7vb; sfaIncidentId=c69b0ec2-ae53-4464-8e4e-17a0c31d376c-BM; JSESSIONID=0001ZMC-OVIte_ihzeTtmQnc_wL:1fa6c5imv',
        'Sec-Fetch-Dest': 'document',
        'Sec-Fetch-Mode': 'navigate',
        'Sec-Fetch-Site': 'none',
        'Sec-Fetch-User': '?1',
        'Upgrade-Insecure-Requests': '1',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/106.0.0.0 Safari/537.36',
        'sec-ch-ua': '"Chromium";v="106", "Google Chrome";v="106", "Not;A=Brand";v="99"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"Windows"',
    }
    headers_1 = {
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
        'Accept-Language': 'en-GB,en-US;q=0.9,en;q=0.8',
        'Cache-Control': 'max-age=0',
        'Connection': 'keep-alive',
        # Requests sorts cookies= alphabetically
        'Cookie': 'oam.Flash.RENDERMAP.TOKEN=-15f2o8r7u1; sfaIncidentId=c69b0ec2-ae53-4464-8e4e-17a0c31d376c-BM; JSESSIONID=0001ZMC-OVIte_ihzeTtmQnc_wL:1fa6c5imv',
        'Origin': 'https://www.earlyyears.edu.gov.on.ca',
        'Referer': 'https://www.earlyyears.edu.gov.on.ca/LCCWWeb/childcare/searchResults.xhtml',
        'Sec-Fetch-Dest': 'document',
        'Sec-Fetch-Mode': 'navigate',
        'Sec-Fetch-Site': 'same-origin',
        'Sec-Fetch-User': '?1',
        'Upgrade-Insecure-Requests': '1',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/106.0.0.0 Safari/537.36',
        'sec-ch-ua': '"Chromium";v="106", "Google Chrome";v="106", "Not;A=Brand";v="99"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"Windows"',
    }
    data = {
        'enterAppForm:mapCenterLat': '',
        'enterAppForm:mapCenterLng': '',
        'enterAppForm:searchByRadius': '-1',
        'enterAppForm:cityInputS': '',
        'enterAppForm:langInputS': '',
        'enterAppForm:smartSearchCNamesJSonStr': '["Oshawa, ON","ANGUS","AURORA","Aberfoyle","Acton","Addison","Ailsa Craig","Ajax","Akwesasne","Alexandria","Alfred","Alliston","Almonte","Alvinston","Alymer","Amaranth","Ameliasburg","Ameliasburgh","Amherstburg","Amherstview","Ancaster","Apsley","Arnprior","Arthur","Arva","Astorville","Astra","Athens","Atikokan","Attawapiskat","Avonmore","Aylmer","Ayr","Ayton","Azilda","BARRIE","BOLTON","BRACEBRIDGE","BRAMPTON","Baden","Balmertown","Baltimore","Bancroft","Barrhaven","Barry\'s Bay","Barrys Bay","Batawa","Bath","Beamsville","Beardmore","Bearskin Lake","Beaverton","Beeton","Belle River","Belleville","Belleville, Ontario","Belmont","Berwick","Bethany","Binbrook","Birch Island","Blackstock","Blenheim","Blind River","Bloomfield","Bloomingdale","Blue Mountains","Bobcaygeon","Bonfield","Borden","Bothwell","Bourget","Bowmanville","Bradford","Bradford West Gwillimbury","Bramptom","Brampton,","Brantford","Brantford, On","Brechin","Breslau","Bridgenorth","Brigden","Brighton","Brights Grove","Brockville","Brooklin","Brucefield","Buckhorn","Burford","Burks Falls","Burlington","CALEDON","CAMBRIDGE","Caledon East","Caledon Village","Caledonia","Callander","Cambrige","Camden East","Cameron","Camlachie","Campbelford","Campbellcroft","Campbellford","Campbellville","Cannington","Capreol","Carleton Place","Carlisle","Carp","Casselman","Castleton","Cavan","Cayuga","Chalk River","Chapleau","Chatham","Chatham-Kent","Chelmsford","Chesley","Chesterville","Christian Island","City of Pickering","Clarence Creek","Clarence-Rockland","Clarington.","Clarmont","Clifford","Clinton","Cloyne","Cobalt","Cobourg","Cochrane","Colborne","Coldwater","Collingwood","Comber","Concord","Conestogo","Coniston","Constance Lake","Cookstown","Copetown","Copper Cliff","Corbeil","Cornwall","Corunna","Cottam","Cottom","Courtice","Courtland","Creemore","Crysler","Crystal Beach","Cumberland","Cumberland Beach","Curve Lake","Cutler","Dalkeith","Dashwood","Deep River","Deer Lake","Delaware","Delhi","Desbarats","Deseronto","Devlin","Dorchester","Douro","Dowling","Downeyville","Downsview","Drayton","Dresden","Drumbo","Dryden","Dubreuilville","Dunchurch","Dundalk","Dundas","Dunnville","Dunsford","Duntroon","Durham","Dutton","Dwight","ETOBICOKE","Ear Falls","Earlton","East Garafraxa","East Gwillimbury","East York","Echo Bay","Eganville","Egbert","Elgin","Elginburg","Elk Lake","Elliot Lake","Elmira","Elmsdale","Elmvale","Elora","Embro","Embrun","Emeryville","Emo","Emsdale","Emsdale\\/Perry Township","Englehart","Enniskillen","Ennismore","Erin","Espanola","Essex","Etobcoke","Everett","Exeter","Fenelon Falls","Fenwick","Fergus","Flamborough","Flesherton","Fonthill","Forest","Fort Albany","Fort Erie","Fort Frances","Foxboro","Frankford","Freelton","Gananoque","Garden River","Garden Village","Garson","Georgetown","Georgetown, Halton Hills","Georgina Island","Geraldton","Glen Morris","Glen Williams","Glenburnie","Glencoe","Gloucester","Goderich","Golden Lake","Goodwood","Gore Bay","Gores Landing","Gorham","Gormley","Gorrie","Goulais River","Gowanstown","Grafton","Grand Bend","Grand Valley","Grassy Narrows","Gravenhurst","Greely","Greenbank","Greensville","Greenwood","Grimsby","Guelph","Gueplh","Guleph","HAMILTON","Hagersville","Haileybury","Haldimand","Haliburton","Halton Hills","Hammond","Hampton","Hanmer","Hannon","Hanover","Harriston","Harrow","Harrowsmith","Hastings","Havelock","Hawkesbury","Hearst","Heathcote","Hensall","Hepworth","Heron Bay","Hickson","Hillsburg","Hillsdale","Holland Centre","Holland Landing","Holstein","Hornby","Hornell Heights","Hornepayne","Huntsville","Hymers","Ignace","Ilderton","Ingersoll","Ingleside","Inglewood","Innerkip","Innisfil","Iroquois","Iroquois Falls","Jarvis","Johnstown","KANATA","KINGSTON","Kakabeka","Kapuskasing","Kars","Kasabonika Lake","Keene","Keene, ON","Keewatin","Kemptville","Kenora","Keswick","Kettle & Stony Point","Kettleby","Kilbride","Killaloe","Kinburn","Kincardine","King City","Kingsville","Kintore","Kirkland Lake","Kitchener","Kitchener, On","Kleinburg","Komoka","L\'Orignal","LaSalle","LaSlle","Lake Temagami","Lakefield","Lakeshore","Langton","Lansdowne","Leamington","Leaside","Lefroy","Levack","Limehouse","Limoges","Lincoln","Lindsay","Linwood","Lion\'s Head","Listowel","Little Britain","Little Current","Lively","Londesboro","Londesborough","London","London Ontario","Long Sault","Longlac","Longue Sault","Loretto","Lucan","Lucknow","Lyn","Lyndhurst","M\'Chigeeng","MARKHAM","MILTON","MISSISSAUGA","MOUNT BRYDGES","Mactier","Madoc","Magnetawan","Maidstone","Mallorytown","Manitouwadge","Manitowaning","Manotick","Maple","Marathon","Marhkham","Mariposa","Markdale","Markstay","Marmora","Massey","Mattawa","Maxwell","Maynooth","Meaford","Merlin","Merrickville","Metcalfe","Middlesex","Midhurst","Midland","Migisi Sahgaigan","Mildmay","Millbrook","Millgrove","Milton, ON","Milverton","Mindemoya","Minden","Minesing","Missisauga","Mississagua","Mississauga City","Mississaugua","Misssissuaga","Mitchell","Monkton","Mono","Mooretown","Moose Creek","Moose Factory","Moosonee","Morrisburg","Mount Albert","Mount Forest","Mount Hope","Mt Carmel","Mulmur","Muncey","Munster Hamlet","Muskrat Dam","NEWMARKET","NORTH YORK","Nakina","Napanee","Nation","Nepean","Nestor Falls","New Dundee","New Hamburg","New Liskeard","New Lowell","New Tecumseth","Newcastle","Newmarket`","Neyaashiinigmiing","Niagara Falls","Niagara on the Lake","Niagara-On-The-Lake","Nigigoonsiminikaanin","Nipigon","Nipissing","Nobel","Nobleton","Noelville","North Bay","North Cobalt","North Gower","North Lancaster","North Oshawa","North York ON","NorthYork","Norval","Norwich","Norwood","Nottawa","OAKVILLE","OSHAWA","Oakville\\/Halton","Odessa","Ohsweken","Omemee","Orangeville","Orillia","Orleans","Orléans","Oro Medonte","Oro Station","Oro-Medonte","Orono","Osgoode","Oshawa On","Otonabee","Ottawa","Owen Sound","Owen Sound, On","Oxford on Rideau","Pain Court","Paisley","Pakenham","Palmerston","Paris","Parkhill","Parry Sound","Pawitik","Pelham","Pembroke","Penetanguishene","Perry","Perth","Petawawa","Peterborough","Petrolia","Pic Mobert","Pickerel","Pickering","Picton","Picton, ON","Pikangikum","Plantagenet","Plattsville","Point Edward","Porcupine","Port Burwell","Port Carling","Port Colborne","Port Dover","Port Elgin","Port Hope","Port Lambton","Port Mcnicoll","Port Perry","Port Rowan","Port Stanley","Port Sydney","Powassan","Prescott","Prince Albert","Puslinch","Queensville","Quinte West","RR#1 St.Thomas","Rainy River","Rama","Ramara","Ramara Township","Red Lake","Redbridge","Renfrew","Richmond","Richmond Hill","Ridgetown","Ridgeway","Ripley","River Canard","River Valley","Rockcliffe","Rockland","Rockton","Rockwood","Rodney","Roseneath","Russell","Ruthven","SCHOMBERG","ST CATHARINES","STAYNER","Saint Albert","Saint-Albert","Sandford","Sandwich South","Sarnia","Sarnia-Lambton","Sauble Beach","Sault Ste Marie","Sault Ste Marie ON","Sault Ste. Marie","Sault Ste.Marie","Scaborough","Scarborough","Scarbrough","Schumacher","Scotland","Seaforth","Selby","Selwyn","Severn Bridge","Shakespeare","Shannonville","Shanty Bay","Sharbot Lake","Sharon","Sheffield","Shelburne","Shoal Lake","Shuniah","Simcoe","Sioux Lookout","Slate River","Smith Falls","Smiths Falls","Smithville","Sombra","Sophiasburg","South Mountain","South Porcupine","South River","South Woodslee","Southampton","Southwold","Sparta","Spencerville","Springfield","St Andrews West","St-Albert","St-Charles","St-Eugène","St-Isidore","St-Pascal-Baylon","St. Catharines","St. Catharnies","St. Clair Beach","St. Clements","St. David\'s","St. George","St. Jacobs","St. Joachim","St. Marys","St. Regis","St. Thomas","St.Catharines","Stevensville","Stirling","Stittsville","Stone Mills Township","Stoney Creek","Stoney Point","Stouffville","Straffordville","Stratford","Strathroy","Stroud","Sturgeon Falls","Sudbury","Sunderland","Sundridge","Sutton","Sutton West","Sydenham","TORONTO","TOTTENHAM","Tara","Tavistock","Tecumseh","Teeterville","Temagami","Temiskaming Shores","Terra Cotta","Terrace Bay","Thamesford","Thamesville","Thedford","Thessalon","Thornbury","Thorndale","Thornhill","Thornloe","Thorold","Thronhill","Thunder Bay","Tilbury","Tillsonburg","Timmins","Tiny","Tiverton","Tobermory","Toronto Ontario","Toronto.","Townsend","Trenton","Troy","Tweed","UNIONVILLE","Utterson","Uxbridge","Val Caron","Val Therese","Vanier","Vankleek Hill","Vars","Vaughan","Vermillion Bay","Verner","Victoria Harbour","Vineland","Virginiatown","WHITBY","Wainfleet","Walkerton","Wallaceburg","Walton","Warkworth","Warminster","Warren","Warsaw","Wasaga Beach","Washago","Waterdown","Waterford","Waterloo","Waterloo, ON","Watford","Wawa","Welland","Welland Ont","Wellesley","Wellington","Wendover","West Lorne","Westport","Wheatley","Whitchurch-Stouffville","White River","Whitedog","Whitefish","Whitney","Wiarton","Wikwemikong","Williamstown","Willowdale","Winchester","Windsor","Wingham","Winona","Woodbridge","Woodlawn","Woodslee","Woodstock","Woodville","Wunnumin","Wyoming","Zurich"]',
        'enterAppForm:smartSearchByLangNamesJSonStr': '["ACHOLI","AFRIKAANS","AKAN","ALBANIAN","AMERICAN SIGN LANGUAGE","AMHARIC","ARABIC","ARMENIAN","ASSYRIAN","AZARI","BENGALI","BISLAMA","BOSNIAN","BULGARIAN","BURMESE","CAMBODIAN","CANTONESE","CATALAN","CEBUANO","CHAVACANO","CHEWA","CHINESE","CHITUMBUKA","CREOLE","CROATIAN","CZECH","DAGAARE","DANISH","DARI","DUTCH","ERITREAN","ESPERANTO","ESTONIAN","ETHIOPIAN","FARSI","FILIPINO","FINNISH","FLEMISH","FRISIAN","FUKIEN","GA","GA-ADANGME-KROBO","GAELIC","GANDA","GEORGIAN","GERMAN","GHANA","GREEK","GUJARATI","HAKKA","HAUSA","HEBREW","HINDI","HUNGARIAN","IBIBIO","IBO","ICELANDIC","IDOMA","IGBO","ILOCANO","INDONESIAN","IRANIAN","ITALIAN","JAMAICAN CREOLE","JAPANESE","KAAMBA","KABYLE","KACHCHI","KANNADA","KASHMIRI","KONKANI","KOREAN","KURDI","LAO","LATVIAN","LINGALA","LITHUANIAN","MACEDONIAN","MAIGACHE","MALAY","MALAYALAM","MALTESE","MANDARIN","MARATHI","NEPALI","NORWEGIAN","NZEMA","OJIBWA","ORIYA","PANJABI\\/PUNJABI","PAPIAMENTO","PERSIAN","POLISH","PORTUGUESE","PUSHTO","QUECHUA","ROMANIAN","RUSSIAN","SAMOAN","SERBIAN","SESOTHO","SINDHI","SINHALA","SINHALESE","SLOVAK","SLOVENIAN","SOGA","SOMALIAN","SPANISH","SWAHILI","SWATOW","SWEDISH","TAGALOG","TAIWANESE","TAMIL","TELUGU","THAI","TIGRIGNA","TIV","TOK PISIN","TULU","TURKISH","UKRAINIAN","URDU","VIETNAMESE","VISAYAN","WELSH","XHOSA","YIDDISH","YORUBA"]',
        'enterAppForm:global': '',
        'enterAppForm:cityInput': '',
        'enterAppForm:streetName': '',
        'enterAppForm:postalCode': '',
        'enterAppForm:typeOfProgram': 'CCCB',
        'enterAppForm:ageGroup': [
            'Infant',
            'Toddler',
            'Preschool',
        ],
        'enterAppForm:j_id__v_254': '1',
        'enterAppForm:langInput': '',
        'enterAppForm:nameOfCCCAndHCCA': '',
        'enterAppForm:search': 'Search Results by List',
        'enterAppForm_SUBMIT': '1',
        'javax.faces.ViewState': 'rSRlB6/h72et4LOzAuiSdZalDsJHJgKFAq034y8UdanezZ8lELWBJXYeq1AYsypfxaj6gg==',
    }
    detail_payload = {
        'enterAppForm:currentPageIndex': '1',
        'enterAppForm:targetPageIndex': '0',
        'enterAppForm:sortBy': '',
        'enterAppForm_SUBMIT': '1',
        'javax.faces.ViewState': 'rSRlB6/h72et4LOzAuiSdf2rwkBHa89WAq034y8UdandJ+1bCex7gzBalI25FWBmWjfj5A==',
        'enterAppForm:_idcl': 'enterAppForm:programList:0:0:j_id__v_233',
    }
    pagination_data = {
        'enterAppForm:currentPageIndex': '1',
        'enterAppForm:targetPageIndex': '2',
        'enterAppForm:sortBy': '',
        'enterAppForm_SUBMIT': '1',
        'javax.faces.ViewState': 'rSRlB6/h72et4LOzAuiSdYSWtRXiSjlQAq034y8UdakgrtonATYNZR+vVrgPaPecE9/REQ==',
        'enterAppForm:_idcl': 'enterAppForm:pageNumberList:1:gotoPage',
    }
    custom_settings = {
        'FEED_URI': 'earlyyears.csv',
        'FEED_FORMAT': 'csv',
        'FEED_EXPORT_ENCODING': 'utf-8-sig',
    }

    def start_requests(self):
        yield scrapy.Request(url='https://www.earlyyears.edu.gov.on.ca/LCCWWeb/childcare/search.xhtml',
                             callback=self.parse, headers=self.headers)

    def parse(self, response, **kwargs):
        view_state = response.xpath("//input[@id='javax.faces.ViewState']/@value").get('')
        data = self.data
        data['javax.faces.ViewState'] = view_state
        yield scrapy.FormRequest(url='https://www.earlyyears.edu.gov.on.ca/LCCWWeb/childcare/search.xhtml',
                                 formdata=data, method='POST', headers=self.headers, callback=self.parse_listing)

    def parse_listing(self, response):
        view_state = response.xpath("//input[@id='javax.faces.ViewState']/@value").get('')
        detail_urls = response.xpath("//a[span/text()='View ']/@onclick").getall()
        for detail_url in detail_urls:
            detail_id = detail_url.split("enterAppForm','")[1].split("');")[0]
            data = deepcopy(self.detail_payload)
            data['javax.faces.ViewState'] = view_state
            data['enterAppForm:_idcl'] = detail_id
            yield scrapy.FormRequest(url='https://www.earlyyears.edu.gov.on.ca/LCCWWeb/childcare/searchResults.xhtml',
                                     formdata=data, method='POST', headers=self.headers, callback=self.parse_details)

        # next_page = response.xpath("//a[@class='inactiveLink']/following-sibling::a[1]")
        # if next_page:
        #     number = next_page.xpath("./span[2]/text()").get('').strip()
        #     name = next_page.xpath("./@name").get('').strip()
        #     data = deepcopy(self.pagination_data)
        #     data['javax.faces.ViewState'] = view_state
        #     data['enterAppForm:targetPageIndex'] = number
        #     data['enterAppForm:_idcl'] = name
        #     print(number)
        #     yield scrapy.FormRequest(url='https://www.earlyyears.edu.gov.on.ca/LCCWWeb/childcare/searchResults.xhtml',
        #                              formdata=data, method='POST', headers=self.headers_1, callback=self.parse_listing)

    def parse_details(self, response):
        yield {
            'Name Of Licensee': response.xpath(
                '//th[contains(b/a/span/text(),"Name of Licensee")]/following-sibling::td/text()').get('').strip(),
            'Address': ''.join(
                response.xpath("//th[contains(b/text(),'Address')]/following-sibling::td/text()").getall()).strip().replace('\n', '').replace('\t', ''),
            'Phone Number': response.xpath('//th[contains(b/text(),"Phone")]/following-sibling::td/text()').get().strip(),
            'Website': response.xpath("//th[contains(b/text(),'Website:')]/following-sibling::td/text()").get(
                '').strip(),

        }
