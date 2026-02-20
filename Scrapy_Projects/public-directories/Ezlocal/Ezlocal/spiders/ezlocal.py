import csv
import os
import re
import urllib
from typing import Iterable

import scrapy
import tkinter as tk
from tkinter import messagebox
from scrapy import Request


class EzlocalSpider(scrapy.Spider):
    name = "ezlocal"
    headers =  {
    'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
    'accept-language': 'en-US,en;q=0.9',
    'cache-control': 'max-age=0',
    # 'cookie': '_ga=GA1.1.1396222623.1741141151; ASP.NET_SessionId=qc3bsywxtlqc0ya2gzp4rccf; ARRAffinity=cb90e21fca87989fb1d569d7f567fbdf8a65d258e36f704a590b7b7a1862b29b; ARRAffinitySameSite=cb90e21fca87989fb1d569d7f567fbdf8a65d258e36f704a590b7b7a1862b29b; cf_clearance=7w4DdfLtka3q.4Kr8YzI5LOMxhyrVs_7i5McbDT8Mcw-1741186093-1.2.1.1-B5oTXMsxwnktJ9R0aJuHoUm3GElU_PAKC4wEjhqKvHS77zvZeOYM7RmJQY2wCa0yf6rjTBV3OrUl1fah2uG08VQJouNIjFfTEaBmrPFUOxLqW_xaSJ0ytg_tNzpeX31ZTWHMB0kInb7sFibLDjBj4sZUuoaRIYe2Kyyu93qMivVrxFX3_3GDXkOH8jZR7msKGWLUHRtGS9XyjogqxtunnKxiO5zqKmc9to8j3rwVVFO5MVE45hCjTxuTRr627A8fMeY6ltLIqsEY8F1vL0BytKMf0KefsQS2ZnnBv8obYCqG6V4qqjyEqjPSkkHc8akHv6Ezwr1lwdx5_k9yzUHuGMsR8fQfGPOGnbWLkaursrA.dP5GvKJxfkTJYayAk7B3LIfiBrPscbTHNbulTaTmeUVKyD7Niv_uXaQK9eKmxX4; __gads=ID=58dab2a7f90b78ba:T=1741141151:RT=1741186445:S=ALNI_MZMerjc-86qo-JmIJT2r6O_8sd8AA; __gpi=UID=00000ffaaec7816f:T=1741141151:RT=1741186445:S=ALNI_MZDz0dH-7muFr9-v5o5dEQXfCvAkg; __eoi=ID=f0b4675b64d320c4:T=1741141151:RT=1741186445:S=AA-AfjZ4nadwzeFLFThhVX5ns27y; _ga_H3F2NE2GYD=GS1.1.1741186094.3.1.1741186448.59.0.0',
    'priority': 'u=0, i',
    'sec-ch-ua': '"Not A(Brand";v="8", "Chromium";v="132", "Google Chrome";v="132"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"Windows"',
    'sec-fetch-dest': 'document',
    'sec-fetch-mode': 'navigate',
    'sec-fetch-site': 'none',
    'sec-fetch-user': '?1',
    'upgrade-insecure-requests': '1',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/132.0.0.0 Safari/537.36',
}
    url = 'https://ezlocal.com/{}/{}/{}'
    base_url = 'https://ezlocal.com{}'

    def get_proxy_url(self, url):
        payload = {'api_key': 'c451120ba44798cb8c7c2fc7c63e2cc9', 'url': url}
        proxy_url = 'https://api.scraperapi.com/?' + urllib.parse.urlencode(payload)
        return proxy_url

    def start_requests(self) -> Iterable[Request]:
        keyword, location = self.get_input()
        city = location.split(',')[0].strip()
        state = location.split(',')[-1].strip()
        keyword_refin = keyword.replace(' ', '-').lower()
        city_refin = city.replace(' ', '-').lower()
        request_url = self.url.format(state.lower(), city_refin, keyword_refin)
        proxy_url = self.get_proxy_url(request_url)
        yield scrapy.Request(url=proxy_url,
                             meta={'Keyword': keyword_refin, 'city': location})

    def parse(self, response):
        keyword = response.meta['Keyword']
        location = response.meta['city']
        file_name = f'{keyword.title()}_{location.replace(",", "").replace(" ", "-").lower()}.csv'
        for data in response.css('div.result'):
            item = dict()
            item['keyword_search'] = keyword
            item['business_name'] = data.css('h3.fw-bold::text').re_first(r'^\d+\.\s*(.*)').strip()
            item['phone_number'] = data.css('p span.fw-bold::text').get('').strip()
            address = ' '.join(data.xpath('.//p/span[not(@class)]/text()').getall()).strip()
            item['address'] = address
            item['zip_code'] = self.extract_zip_code(address)
            url = data.css('div.result a.stretched-link::attr(href)').get('').strip()
            item['URL'] = self.base_url.format(url)
            self.append_or_create_csv(f'output/{file_name}', item)

        next_page = response.xpath('//li/a[contains(text(),"»")]/@href').get()
        if next_page:
            proxy_url = self.get_proxy_url(self.base_url.format(next_page))
            yield scrapy.Request(url=proxy_url,headers=self.headers,
                                 meta={'Keyword': keyword, 'city': location})

            # print(item)

    def get_input(self):
        def submit():
            nonlocal keyword, location
            keyword = keyword_entry.get().strip()
            location = location_entry.get().strip()

            if not keyword or not location:
                messagebox.showerror("Input Error", "Both Keyword and Location fields are required!")
                return

            location_pattern = r"^[A-Za-z ]+, [A-Za-z]{2}$"
            if not re.match(location_pattern, location):
                messagebox.showerror("Input Error", "Location must be in the format: City, State (e.g., New York, NY)")
                return

            root.destroy()

        root = tk.Tk()
        root.title("Search Input Form")

        window_width = 750
        window_height = 350
        screen_width = root.winfo_screenwidth()
        screen_height = root.winfo_screenheight()
        position_x = (screen_width // 2) - (window_width // 2)
        position_y = (screen_height // 2) - (window_height // 2)
        root.geometry(f"{window_width}x{window_height}+{position_x}+{position_y}")

        root.configure(bg="#f0f0f0")

        tk.Label(root, text="Enter Details", font=("Arial", 16, "bold"), bg="#f0f0f0").pack(pady=15)

        frame = tk.Frame(root, bg="#ffffff", padx=20, pady=20, relief=tk.RIDGE, borderwidth=2)
        frame.pack(pady=10)

        tk.Label(frame, text="Keyword:", font=("Arial", 12), bg="#ffffff").grid(row=0, column=0, sticky="w", pady=5)
        keyword_entry = tk.Entry(frame, width=40, font=("Arial", 12))
        keyword_entry.grid(row=0, column=1, pady=5)

        tk.Label(frame, text="Location (i.e. New York, NY):", font=("Arial", 12), bg="#ffffff").grid(row=1, column=0, sticky="w", pady=5)
        location_entry = tk.Entry(frame, width=40, font=("Arial", 12))
        location_entry.grid(row=1, column=1, pady=5)

        submit_btn = tk.Button(root, text="Search", font=("Arial", 12, "bold"), bg="#4CAF50", fg="white", padx=20,
                               pady=5, command=submit)
        submit_btn.pack(pady=20)

        keyword, location = None, None
        root.mainloop()

        return keyword, location

    def append_or_create_csv(self, filename, data_dict):
        # Check if file exists
        try:
            file_exists = os.path.isfile(filename)
            with open(filename, mode='a', newline='', encoding='utf-8') as file:
                writer = csv.DictWriter(file, fieldnames=data_dict.keys())
                if not file_exists:
                    writer.writeheader()

                # Write data row
                writer.writerow(data_dict)
                print('Data Added!!!')
        except Exception as ex:
            print(f'Error!!! {ex}')

    def extract_zip_code(self, address: str) -> str:
        """Extracts the ZIP code from a given address string."""
        match = re.search(r'\b\d{5}(?:-\d{4})?\b', address)
        return match.group() if match else None
