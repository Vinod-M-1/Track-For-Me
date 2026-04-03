import re
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

def get_price(url):
    options = Options()
    options.add_argument("--headless") # Run without opening a window
    options.add_argument("--disable-blink-features=AutomationControlled")
    # Crucial: Myntra and Flipkart often block default Selenium User-Agents
    options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36")

    driver = None
    price_str = "Price not found"

    try:
        driver = webdriver.Chrome(
            service=Service(ChromeDriverManager().install()),
            options=options
        )
        driver.get(url)
        wait = WebDriverWait(driver, 15) # Increased wait time for slower sites

        if "amazon" in url:
            # Try 3 different ways to find the price on Amazon
            try:
                # 1. Try the 'offscreen' price (it's often hidden but contains the full value)
                # We use a CSS Selector to find the span inside the price display
                wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, ".a-price .a-offscreen")))
                price_str = driver.find_element(By.CSS_SELECTOR, ".a-price .a-offscreen").get_attribute("innerText")
            except:
                try:
                    # 2. Fallback to your original 'whole' and 'fraction' method
                    wait.until(EC.presence_of_element_located((By.CLASS_NAME, "a-price-whole")))
                    whole = driver.find_element(By.CLASS_NAME, "a-price-whole").text
                    try:
                        fraction = driver.find_element(By.CLASS_NAME, "a-price-fraction").text
                    except:
                        fraction = "00"
                    price_str = f"{whole}.{fraction}"
                except:
                    # 3. Final attempt: Look for any large price text
                    try:
                        price_str = driver.find_element(By.ID, "price_inside_buybox").text
                    except:
                        price_str = "Price not found"
        elif "flipkart" in url:
            # Try specific class first, then general XPath
            try:
                # Wait longer for Flipkart
                wait = WebDriverWait(driver, 20) 
                element = wait.until(EC.presence_of_element_located(
                    (By.XPATH, "//div[contains(@class, 'Nx9W60')] | //div[contains(@class, '_30jeq3')]")
                ))
                price_str = element.text
            except:
                # If class fails, look for the ₹ symbol anywhere on the page
                try:
                    price_str = driver.find_element(By.XPATH, "//*[contains(text(), '₹')]").text
                except:
                    price_str = "Price not found"

        elif "myntra" in url:
            # Myntra Logic
            wait.until(EC.presence_of_element_located((By.CLASS_NAME, "pdp-price")))
            # Myntate usually displays "Rs. 1499" inside a strong tag
            price_str = driver.find_element(By.CLASS_NAME, "pdp-price").text

        else:
            return "Unsupported Website"

        # --- THE CLEANER ---
        # This regex removes everything except digits and the decimal point
        # Example: "₹18,999.00" -> "18999.00" or "Rs. 1,499" -> "1499"
        clean_price = re.sub(r'[^\d.]', '', price_str)
        
        # If the string is empty after cleaning, return original error
        return clean_price if clean_price else "Price not found"

    except Exception as e:
        print(f"❌ Scraper Error on {url}: {e}")
        return "Price not found"

    finally:
        if driver:
            driver.quit()