from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


def get_price(url):
    options = Options()
    options.add_argument("--headless")
    options.add_argument("--disable-blink-features=AutomationControlled")

    driver = None  # 🔥 important

    try:
        driver = webdriver.Chrome(
            service=Service(ChromeDriverManager().install()),
            options=options
        )

        driver.get(url)

        wait = WebDriverWait(driver, 10)

        # Wait for price container
        wait.until(
            EC.presence_of_element_located((By.ID, "corePriceDisplay_desktop_feature_div"))
        )

        print("Page title:", driver.title)

        try:
            whole = driver.find_element(By.CLASS_NAME, "a-price-whole").text
            fraction = driver.find_element(By.CLASS_NAME, "a-price-fraction").text
            price = whole.replace(",", "") + "." + fraction
        except:
            price = "Price not found"

    except Exception as e:
        print("❌ Selenium Error:", e)
        price = "Price not found"

    finally:
        if driver:
            driver.quit()   # ✅ only once

    return price