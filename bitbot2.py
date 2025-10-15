import time
import os
import sys
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

options = Options()
options.add_argument("--headless")
options.set_preference("dom.webdriver.enabled", False)
options.set_preference("useAutomationExtension", False)
options.set_preference("media.volume_scale", "0.0")  # Mute audio if any

# === CONFIGURATION ===
screenshot_dir = os.path.expanduser("~/bitbot/Screenshots")
timeframes = ['15m', '1h', '4h']

os.makedirs(screenshot_dir, exist_ok=True)

driver = webdriver.Firefox(options=options)

symbol = sys.argv[1] if len(sys.argv) > 1 else "BTCUSDT"
driver.get(f"https://www.bitunix.com/spot-trade/{symbol}")

wait = WebDriverWait(driver, 20)

ul_element = wait.until(EC.presence_of_element_located((
    By.XPATH, "/html/body/div[1]/div[4]/div/section/div/div[1]/section[2]/div/div[2]/div/div[1]/div/div/div/div/div/div/div[1]/div/div[2]/div[2]/ul")))

try:
    fullscreen_btn = wait.until(EC.element_to_be_clickable((
        By.XPATH, "/html/body/div[1]/div[4]/div/section/div/div[1]/section[2]/div/div[2]/div/div[1]/div/div/div/div/div/div/div[1]/div/div[3]"
    )))
    fullscreen_btn.click()
    print("️ Fullscreen chart activated.")
except Exception:
    print("⚠️ Fullscreen button not found or clickable. Continuing.")

li_elements = ul_element.find_elements(By.TAG_NAME, "li")
matching_lis = [li for li in li_elements if li.text in timeframes]

def save_chart_screenshot(name):
    try:
        chart_element = driver.find_element(
            By.XPATH, "/html/body/div[1]/div[4]/div/section/div/div[1]/section[2]"
        )
        filepath = os.path.join(screenshot_dir, f"{name}.png")
        chart_element.screenshot(filepath)
        print(f" Saved screenshot: {filepath}")
    except Exception as e:
        print(f"❌ Failed to capture screenshot for {name}: {e}")

for li in matching_lis:
    tf_name = li.text
    print(f"️ Clicking: {tf_name}")
    try:
        li.click()
        time.sleep(3)
        save_chart_screenshot(tf_name)
    except Exception as e:
        print(f"⚠️ Error handling timeframe {tf_name}: {e}")

driver.quit()
