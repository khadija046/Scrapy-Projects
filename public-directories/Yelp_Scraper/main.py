from time import sleep

from utils.app import pause_for_user, confirm_dialog, type_like_human, write_dict_to_csv
import undetected_chromedriver as uc

from selenium.common import (
    TimeoutException,
    NoSuchElementException,
    WebDriverException
)
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait


# ----------------------- SELENIUM -----------------------

def configure_selenium_driver():
    print("🚀 Initializing Selenium driver...")
    try:
        options = uc.ChromeOptions()
        options.add_argument("--disable-blink-features=AutomationControlled")
        options.add_argument("--no-sandbox")
        options.add_argument("--disable-gpu")

        driver = uc.Chrome(
            options=options,
            headless=False,
            use_subprocess=True
        )
        driver.maximize_window()
        print("✅ Browser launched successfully")
        return driver

    except Exception as e:
        print(f"[ERROR] Driver init failed: {e}")
        return None


def scrape_current_page(driver):
    print("\n📄 Scraping current results page...")
    original_window = driver.current_window_handle
    records = driver.find_elements(By.XPATH, '//div[contains(@class,"businessName")]/h3/a')

    print(f"🔍 Found {len(records)} business listings")

    for index, record in enumerate(records[:], start=1):
        item = {}
        print(f"\n➡️ Opening business {index}")

        try:
            sleep(1)
            record.click()

            WebDriverWait(driver, 10).until(lambda d: len(d.window_handles) > 1)

            for handle in driver.window_handles:
                if handle != original_window:
                    driver.switch_to.window(handle)
                    break

            print("🆕 Switched to business tab")
            sleep(3)

            item["restaurantName"] = driver.find_element(By.XPATH, "//div/h1").text.strip()
            print(f"🏷 Name: {item['restaurantName']}")

            try:
                website = driver.find_element(
                    By.XPATH,
                    '//p[contains(text(),"Business website")]/following-sibling::p/a'
                )
                raw = website.get_attribute("href")
                clean = raw.split("url=")[-1].split("&")[0]
                item["websiteUrl"] = clean.replace('%3A', ':').replace('%2F', '/')
                print(f"🌐 Website found: {item['websiteUrl']}")
            except NoSuchElementException:
                item["websiteUrl"] = ""
                print("⚠️ Website not available")

            write_dict_to_csv("output/Yelp_data.csv", item)
            print("💾 Data saved to CSV")

        except Exception as e:
            print(f"[ERROR] Record failed: {e}")

        finally:
            if len(driver.window_handles) > 1:
                driver.close()
                driver.switch_to.window(original_window)
                print("↩️ Returned to results page")
            sleep(2)


def handle_pagination(driver):
    print("\n🔎 Checking for next page...")
    try:
        driver.find_element(By.CSS_SELECTOR, 'a[aria-label="Next"]')
        print("📄 Next page detected")

        proceed = confirm_dialog(
            title="Pagination Detected",
            header="📄 More Results Available",
            message=(
                "Another page of Yelp results is available.\n\n"
                "Please open the next page\n"
                "and continue scraping?"
            )
        )

        if not proceed:
            print("⛔ User stopped pagination")
            return False

        print("➡️ User chose to continue to next page")
        return True

    except NoSuchElementException:
        print("✅ No more pages available")
        return False


# ----------------------- MAIN FLOW -----------------------

def yelp_request():
    print("🧠 Starting Yelp scraper")
    driver = configure_selenium_driver()
    if not driver:
        print("❌ Driver not available. Exiting.")
        return

    try:
        print("🌐 Opening Google")
        driver.get("https://www.google.com")

        search = WebDriverWait(driver, 20).until(
            EC.presence_of_element_located((By.NAME, "q"))
        )
        print("⌨️ Searching for yelp.com")
        type_like_human(search, "yelp.com")
        search.submit()

        first = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, '//a[contains(@href, "yelp.com")]/h3'))
        )
        print("🔗 Opening Yelp")
        first.click()

        sleep(8)
        print("⏸ Waiting for user input (keyword & location)")
        pause_for_user()
        print("▶️ Scraper resumed")

        while True:
            scrape_current_page(driver)
            if not handle_pagination(driver):
                break

        print("🏁 Scraping completed")

    except (TimeoutException, WebDriverException) as e:
        print(f"[ERROR] Runtime failure: {e}")

    finally:
        print("🧹 Closing browser")
        driver.quit()
        print("✅ Scraper finished cleanly")


if __name__ == "__main__":
    yelp_request()
