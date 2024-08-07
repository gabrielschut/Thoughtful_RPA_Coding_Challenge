import pandas as pd
import time

from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By

service = Service()
options = webdriver.ChromeOptions()
driver = webdriver.Chrome(service= service, options= options)
try:
    driver.maximize_window()
    driver.get("https://apnews.com/")
    time.sleep(5)
    driver.find_element(By.CLASS_NAME, 'SearchOverlay-search-button').click()
    time.sleep(5)
    searchbar = driver.find_element(By.CLASS_NAME, 'SearchOverlay-search-label')
    searchbar.send_keys('Trump')
    searchbar.send_keys(Keys.ENTER)
    time.sleep(5)

finally:
    driver.quit()