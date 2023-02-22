from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import time


ser = Service("C:/Python/Python310/Udemy/Chromedriver/chromedriver.exe")
op = webdriver.ChromeOptions()

driver = webdriver.Chrome(service=ser, options=op)
driver.get("http://orteil.dashnet.org/experiments/cookie/")

cookie_button = driver.find_element(By.CSS_SELECTOR, "#cookie")

upgrades = driver.find_elements(By.CSS_SELECTOR, "#store div")
upgrade_ids = [item.get_attribute("id") for item in upgrades]

upgrade = time.time() + 8
timeout = time.time() + 60*5


while True:
    cookie_button.click()

    if time.time() > upgrade:

        all_prices = driver.find_elements(By.CSS_SELECTOR, "#store b")
        prices = []
        for price in all_prices:
            text = price.text
            if text != "":
                cost = int(text.split("-")[1].replace(",", ""))
                prices.append(cost)

        cookie_upgrades = {}
        for n in range(len(prices)):
            cookie_upgrades[prices[n]] = f"#{upgrade_ids[n]}"

        money_element = driver.find_element(By.CSS_SELECTOR, "#money").text
        if "," in money_element:
            money_element = money_element.replace(",", "")
        cookie_count = int(money_element)

        affordable_upgrades = {}
        for cost, id in cookie_upgrades.items():
            if cookie_count > cost:
                affordable_upgrades[cost] = id
        try:
            best_upgrade = max(affordable_upgrades)
            id_of_best_upgrade = cookie_upgrades[best_upgrade]
            driver.find_element(By.CSS_SELECTOR, id_of_best_upgrade).click()
        except ValueError:
            pass
        upgrade = time.time() + 8


driver.quit()
