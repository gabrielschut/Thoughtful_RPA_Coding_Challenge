import pandas as pd
import time

from SeleniumUtils import driver_factory
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By


driver = driver_factory.create_driver()
topic = "California"
months = 5
try:
    driver.maximize_window()
    driver.get('https://www.latimes.com/')
    time.sleep(8)
    driver.execute_script('window.scrollBy(0, 900);')
    time.sleep(3)
    driver.find_element(By.CSS_SELECTOR, '[data-element="search-button"]').click()
    time.sleep(3)
    searchbar = driver.find_element(By.CSS_SELECTOR, '[data-element="search-form-input"]')
    searchbar.send_keys('Gold')
    searchbar.send_keys(Keys.ENTER)
    time.sleep(3)
    topics = driver.find_elements(By.CLASS_NAME, 'checkbox-input-label')
    see_all = driver.find_elements(By.CSS_SELECTOR, '[data-toggle-trigger="see-all"]')
    for i in topics:
        if (i.text == topic):
            i.click()
            break
    time.sleep(10)

finally:
    driver.quit()