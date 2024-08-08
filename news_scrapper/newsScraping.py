import pandas as pd
import time
from datetime import date
import re


from utils import driver_factory, last_date
from article import Article

from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By


def contains_money_on_text(title, description):
        pattern = r"""
            (?:
                \$\s?\d{1,3}(?:,\d{3})(?:,\d{3})*(?:\.\d{2})? |  # $11.1, $111,111.11
                \d{1,3}(?:,\d{3})(?:,\d{3})*(?:\.\d{2})?\s?(?:dollars|USD)  # 11 dollars, 11 USD
            )
        """
        # Compiles the regex with the ignore whitespace options
        regex = re.compile(pattern, re.VERBOSE | re.IGNORECASE)
        if (regex.search(title) or regex.search(description)):
            return True
        return False


def count_ocurrences(sear_phrase : str, title : str, description : str):
    ocorrences : int
    ocorrences = title.lower().count(sear_phrase.lower())
    ocorrences += description.lower().count(sear_phrase.lower())
    return ocorrences


driver = driver_factory.create_driver()
topic = "California"
months = -1
searsh_term = 'Gold'
article_list = []
try:
    driver.maximize_window()
    driver.get('https://www.latimes.com/')
    time.sleep(8)
    driver.execute_script('window.scrollBy(0, 900);')
    time.sleep(3)
    driver.find_element(By.CSS_SELECTOR, '[data-element="search-button"]').click()
    time.sleep(3)
    searchbar = driver.find_element(By.CSS_SELECTOR, '[data-element="search-form-input"]')
    searchbar.send_keys(searsh_term)
    searchbar.send_keys(Keys.ENTER)
    time.sleep(3)
    topics = driver.find_elements(By.CLASS_NAME, 'checkbox-input-label')
    see_all = driver.find_elements(By.CSS_SELECTOR, '[data-toggle-trigger="see-all"]')
    for i in topics:
        if (i.text == topic):
            i.click()
            break
    time.sleep(3)
    next_page = True
    while next_page:
        articles = driver.find_elements(By.CLASS_NAME, 'promo-wrapper')
        for i in articles:
            timestamp_elemento = driver.find_element(By.CSS_SELECTOR, 'p.promo-timestamp')
            timestamp = timestamp_elemento.get_attribute('data-timestamp')
            publich_date = date.fromtimestamp(int(timestamp) / 1000)
            if (last_date.is_before(publich_date,months)):
                next_page = False
                break
            
            title = aria_label = driver.find_element(By.CSS_SELECTOR, '.promo-wrapper .promo-media a').get_attribute('aria-label')
            description = description = driver.find_element(By.CSS_SELECTOR, '.promo-wrapper .promo-description').text
            imagem = driver.find_element(By.CSS_SELECTOR, 'div.promo-media picture img')
            picture_file_name = imagem.get_attribute('alt')
            money_on_text = contains_money_on_text(title,description)
            times_search_term_appears = count_ocurrences(searsh_term,title, description)
            article_list.append(Article(title,publich_date,description,picture_file_name, money_on_text,times_search_term_appears))
        driver.find_element(By.CLASS_NAME, 'search-results-module-next-page').click()
        time.sleep(3)
finally:
    driver.quit()
    final_list = article_list


