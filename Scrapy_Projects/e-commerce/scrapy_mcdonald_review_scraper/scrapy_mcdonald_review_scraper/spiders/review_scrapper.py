import sys

import scrapy
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By


class ReviewScrapperSpider(scrapy.Spider):
    name = 'review_scrapper'
    request_url = 'https://www.google.com/maps/place/McDonalds/@32.5828738,73.8208346,' \
                  '10z/data=!4m11!1m2!2m1!1sMcDonalds!3m7!1s0x391f1913d6ca092d:0xa9f422bcc87388f!8m2!3d32.4783757' \
                  '!4d74.0922284!9m1!1b1' \
                  '!15sCgpNY0RvbmFsZCdzIgOIAQFaDCIKbWNkb25hbGQnc5IBFGZhc3RfZm9vZF9yZXN0YXVyYW50mgEkQ2hkRFNVaE5NRzlu' \
                  'UzBWSlEwRm5TVVJOY0RseFlqWjNSUkFC4AEA '

    def start_requests(self):
        DRIVER_PATH = 'C:/chromedriver_win32/chromedriver.exe'

        driver = webdriver.Chrome(executable_path=DRIVER_PATH)
        driver.get(self.request_url)
        # driver.page_source
        # h1 = driver.find_element(By.XPATH, '//*[@id="ChdDSUhNMG9nS0VJQ0FnSUNnNzRqNl93RRAB"]/span[2]/text()')
        print(driver.title)

    def parse(self, response):
        h1 = response.find_element(By.XPATH, '//*[@id="ChdDSUhNMG9nS0VJQ0FnSUNnNzRqNl93RRAB"]/span[2]/text()')
        print(response)
        response.quit()

