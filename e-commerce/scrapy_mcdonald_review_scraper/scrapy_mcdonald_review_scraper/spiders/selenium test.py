import csv
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


class DetailSelenium:
    request_url = 'https://www.spears500.com/ranking'
    driver = webdriver.Chrome('C:/chromedriver_win32/chromedriver.exe')
    driver.maximize_window()
    list_check = []
    def get_data(self, driver):
        driver.get(self.request_url)
        scheight = .1
        while scheight < 1.0:
            driver.execute_script("window.scrollTo(0, document.body.scrollHeight*%s);" % scheight)
            scheight += .1
            time.sleep(1)
        try:
            driver.execute_script("arguments[0].scrollIntoView(true);", WebDriverWait(driver, 10).until(
                EC.visibility_of_element_located((By.CSS_SELECTOR,
                                                  "a[id='loadMore']"))))
            driver.execute_script("arguments[0].click();", WebDriverWait(driver, 20).until(EC.element_to_be_clickable((
                                                                                                                      By.CSS_SELECTOR,
                                                                                                                      "a[id='loadMore']"))))
            while True:
                if driver.find_element(By.CSS_SELECTOR, "a[id='loadMore']"):
                    driver.execute_script("arguments[0].scrollIntoView(true);", WebDriverWait(driver, 10).until(
                        EC.visibility_of_element_located((By.CSS_SELECTOR,
                                                          "a[id='loadMore']"))))
                    driver.execute_script("arguments[0].click();",
                                          WebDriverWait(driver, 20).until(EC.element_to_be_clickable((
                                              By.CSS_SELECTOR,
                                              "a[id='loadMore']"))))
                self.get_link(driver)

            # links = driver.find_element(By.CSS_SELECTOR, "a.article")
                # print(driver.find_element(By.CSS_SELECTOR, "a.article").get_attribute('href'))

        except Exception as e:
            print(e)

    def get_link(self, driver):
        lists = driver.find_elements(By.CSS_SELECTOR, "a.article")
        for data in lists:
            item = dict()
            item['website'] = data.get_attribute('href')
            print(item)
            self.list_check.append(item)
        keys = self.list_check[0].keys()
        with open('Phase_3-1_V1.csv', 'w', newline='', encoding='utf-8') as csvfile:
            dict_writer = csv.DictWriter(csvfile, keys)
            dict_writer.writeheader()
            dict_writer.writerows(self.list_check)



if __name__ == '__main__':
    obj = DetailSelenium()
    obj.get_data(driver=obj.driver)

