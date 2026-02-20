import csv
import time
from selenium import webdriver
from selenium.webdriver.common.by import By


class DetailSelenium:
    data_list = []
    request_url = 'https://dappradar.com/rankings/protocol/ethereum/{}'
    chromeOptions = webdriver.ChromeOptions()
    chromedriver = "C:/chromedriver_win32/chromedriver.exe"

    def get_data(self):
        try:
            for index in range(1, 142):
                request_url = self.request_url.format(index)
                time.sleep(2)
                driver = webdriver.Chrome(executable_path=self.chromedriver, chrome_options=self.chromeOptions)
                driver.get(request_url)
                time.sleep(2)
                data = driver.find_elements(By.CSS_SELECTOR, "a.dapp-name-link-comp")
                time.sleep(2)
                for name in data:
                    item = dict()
                    item['Business Site'] = name.get_attribute('href')
                    item['Business Name'] = name.text
                    self.data_list.append(item)
                    print(item)
                driver.quit()
            keys = self.data_list[0].keys()
            with open('dappradar.csv', 'w', newline='', errors='ignore', encoding='') as csvfile:
                dict_writer = csv.DictWriter(csvfile, keys)
                dict_writer.writeheader()
                dict_writer.writerows(self.data_list)
            time.sleep(3)

        except:
            print('error')
            # driver.quit()


if __name__ == '__main__':
    obj = DetailSelenium()
    obj.get_data()
