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

    driver = webdriver.Chrome(
        service=Service(ChromeDriverManager().install()),
        options=options
    )

    driver.get(url)

    try:
        wait = WebDriverWait(driver, 10)

        # 🔥 Wait specifically for price container (IMPORTANT)
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
        print("Error:", e)
        price = "Price not found"

    driver.quit()
    return price

