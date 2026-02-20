import csv
import time
from selenium import webdriver
from selenium.webdriver.common.by import By

def read_csv():
    with open('heinze.csv', 'r') as reader:
        return list(csv.DictReader(reader))


if __name__ == "__main__":
    json_data = read_csv()
    list_data = []
    for data in json_data:
        item = dict()
        detail_url = data.get('Detail_url', '')
        if detail_url:
            chromeOptions = webdriver.ChromeOptions()
            chromedriver = "C:/chromedriver_win32/chromedriver.exe"
            email = ''
            try:
                driver = webdriver.Chrome(executable_path=chromedriver, chrome_options=chromeOptions)
                driver.get(detail_url)
                time.sleep(3)
                driver.find_element(By.CSS_SELECTOR, 'a.cmptxt_btn_yes').click()
                time.sleep(2)
                driver.find_element(By.CSS_SELECTOR, 'a.cssNewASideBlock').click()
                time.sleep(3)
                email = driver.find_element(By.CSS_SELECTOR, 'a[itemprop="email"]')
                time.sleep(2)
                item['Quelle / Link zum Kontakt'] = data.get('Quelle / Link zum Kontakt')
                item['Büro'] = data.get('Büro')
                item['Strasse'] = data.get('Strasse')
                item['PLZ'] = data.get('PLZ')
                item['Stadt'] = data.get('Stadt')
                item['Tel'] = data.get('Tel')
                item['Mail'] = email.text
                item['Personen'] = data.get('Personen')
                item['Anrede'] = data.get('Anrede')
                print(email.text)
                list_data.append(item)
                driver.quit()
            except:
                print('no email')
        else:
            item['Quelle / Link zum Kontakt'] = data.get('Quelle / Link zum Kontakt')
            item['Büro'] = data.get('Büro')
            item['Strasse'] = data.get('Strasse')
            item['PLZ'] = data.get('PLZ')
            item['Stadt'] = data.get('Stadt')
            item['Tel'] = data.get('Tel')
            item['Mail'] = data.get('Mail')
            item['Personen'] = data.get('Personen')
            item['Anrede'] = data.get('Anrede')
            print('from else')
            list_data.append(item)

    keys = list_data[0].keys()
    with open('heinze_V2.csv', 'w', newline='', errors='ignore') as csvfile:
        dict_writer = csv.DictWriter(csvfile, keys)
        dict_writer.writeheader()
        dict_writer.writerows(list_data)

