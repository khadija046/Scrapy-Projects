from selenium import webdriver
from datetime import datetime
from selenium.webdriver.common.by import By
from time import sleep
import pandas as pd
from random import randint

website = """
#########################################
#           WEBSITE: INDEED.FR          #
######################################### 
"""
print(website)
start_time = datetime.now()
print('Crawl starting time : {}'.format(start_time.time()))
print()
job_list = ["data+analyst", "data+scientist", "business+analyst"]

application_links = []
job_titles = []
company_names = []
job_locations = []
application_types = []
publication_dates = []
scraping_dates = []

for job in job_list:

    # opts = webdriver.ChromeOptions()
    # opts.headless = True
    driver = webdriver.Chrome(executable_path="C:/chromedriver_win32/chromedriver.exe")

    driver.get(
        "https://www.indeed.fr/jobs?q=" + job + "&l=Paris+%2875%29&jt=fulltime&limit=50&radius=25&start=0"
    )

    sleep(randint(7, 10))
    print('Collecting data for "{}"...'.format(job))
    # First, get the number of jobs available
    job_number = driver.find_element(By.XPATH, "//div[@id='searchCountPages']").text
    # Calculating number of pages to be crawled (number of jobs available - number of jobs per page (here, 30))
    job_number = job_number.split(" ", 4)
    job_number = int(job_number[3])
    print("- Number of open positions : {}".format(job_number))
    exact_page_nb = job_number / 50
    print("- Exact number of pages to be crawled : {}".format(exact_page_nb))
    min_page_nb = job_number // 50
    print("- Minimum number of pages to be crawled : {}".format(min_page_nb))
    pages = ''
    if exact_page_nb > min_page_nb:
        page_nb = min_page_nb * 50
        pages = [str(i) for i in range(0, page_nb, 50)]
    elif exact_page_nb == min_page_nb:
        page_nb = (min_page_nb - 1) * 50
        pages = [str(i) for i in range(0, page_nb, 50)]

    for page in pages:
        driver.get(
            "https://www.indeed.fr/jobs?q=" + job + "&l=Paris+%2875%29&jt=fulltime&limit=50&radius=25&start=" + page
        )

        sleep(randint(5, 12))

        # Locating job container
        all_cards = driver.find_elements(By.XPATH, "//div[@class='jobsearch-SerpJobCard unifiedRow row result "
                                                   "clickcard']")

        for card in all_cards:

            # Collecting job link
            application_link = card.find_elements(By.CSS_SELECTOR, 'a')
            if not application_link:
                application_link = "Unknown"
            else:
                application_link = application_link[0].get_attribute('href')
            application_links.append(application_link)

            # Collecting job title
            job_title = card.find_elements(By.CSS_SELECTOR, 'a')
            if not job_title:
                job_title = "Unknown"
            else:
                job_title = job_title[0].text
            job_titles.append(job_title)

            # Collecting company name
            company_name = card.find_elements(By.CSS_SELECTOR, 'div.sjcl div span.company')
            if not company_name:
                company_name = "Unknown"
            else:
                company_name = company_name[0].text
            company_names.append(company_name)

            # Collecting job location
            job_location = card.find_elements(By.CSS_SELECTOR, '.location.accessible-contrast-color-location')
            if not job_location:
                job_location = "Unknown"
            else:
                job_location = job_location[0].text
            job_locations.append(job_location)

            # Collecting application type (easy apply)
            application_type = card.find_elements(By.CSS_SELECTOR, '.jobCardShelfContainer')
            if not application_type:
                application_type = "company's website"
            else:
                application_type = application_type[0].text
            application_types.append(application_type)

            # Collecting publication date
            publication_date = card.find_elements(By.CSS_SELECTOR, 'span.date')
            if not publication_date:
                publication_date = "il y a 40 minutes"
            else:
                publication_date = publication_date[0].text
            publication_dates.append(publication_date)

            # Collecting generated scraping time
            scraping_dates.append(datetime.now())

    print('Crawling status for "{}" : Done'.format(job))
    print()

    driver.quit()

print('Crawling time : {}'.format(datetime.now() - start_time))
print('Dataframe successfuly created and exported')

# Dataframe creation
df = pd.DataFrame({'job_title': job_titles,
                   'company_name': company_names,
                   'job_location': job_locations,
                   'application_link': application_links,
                   'publication_date': publication_dates,
                   'application_type': application_types,
                   'scraping_date': scraping_dates
                   })

# ----------------------------------------------------------------------

# Saving .csv file within the "new_datasets" directory
csv_file = 'indeed_data_{}.csv'.format(datetime.now())
df.to_csv(f'spiders/' + csv_file)
