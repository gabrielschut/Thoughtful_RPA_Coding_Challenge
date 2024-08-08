from selenium import webdriver
from selenium.webdriver.chrome.service import Service

@staticmethod
def create_driver():
    service = Service()
    options = webdriver.ChromeOptions()
    driver = webdriver.Chrome(service= service, options= options)
    driver.maximize_window()
    return driver