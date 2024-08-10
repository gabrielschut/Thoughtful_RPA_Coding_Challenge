import time
from datetime import date
import re
import urllib.request

from utils import driver_factory, last_date
from article import Article

from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select


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


def count_ocurrences(search_phrase : str, title : str, description : str):
    ocorrences = title.lower().count(search_phrase.lower())
    ocorrences += description.lower().count(search_phrase.lower())
    return ocorrences


def la_news_scrapper(search_term ,topic, months):
    driver = driver_factory.create_driver()
    article_list = []
    driver.maximize_window()
    driver.get('https://www.latimes.com/')
    time.sleep(5)
    driver.execute_script('window.scrollBy(0, 800);')
    time.sleep(3)
    driver.find_element(By.CSS_SELECTOR, '[data-element="search-button"]').click()
    time.sleep(3)
    searchbar = driver.find_element(By.CSS_SELECTOR, '[data-element="search-form-input"]')
    searchbar.send_keys(search_term)
    searchbar.send_keys(Keys.ENTER)
    time.sleep(3)
    topics = driver.find_elements(By.CLASS_NAME, 'checkbox-input-label')
    see_all = driver.find_elements(By.CSS_SELECTOR, '[data-toggle-trigger="see-all"]')
    if (not topic == '' or topic == None):
        for i in topics:
            if (i.text == topic):
                i.click()
                break
        time.sleep(3)
        
    select_element = driver.find_element(By.CSS_SELECTOR, '.search-results-module-sorts .select-input')
    select = Select(select_element)
    select.select_by_visible_text('Newest') 
    time.sleep(3)
    next_page = True
    while next_page:
        articles = []
        articles = driver.find_elements(By.CLASS_NAME, 'promo-wrapper')
        for i in articles:
            timestamp_elemento = i.find_element(By.CSS_SELECTOR, 'p.promo-timestamp')
            timestamp = timestamp_elemento.get_attribute('data-timestamp')
            publich_date = date.fromtimestamp(int(timestamp) / 1000)
            if (last_date.is_before(publich_date,months)):
                next_page = False
                break
            file_path = 'news_scrapper/pictures'
            title = i.find_element(By.CSS_SELECTOR, '.promo-content .promo-title-container .promo-title a').text
            description = ''
            try:
                description = i.find_element(By.CSS_SELECTOR, '.promo-wrapper .promo-description').text
            except:
                description = ''
            image_file_name = ''
            try:
                image = i.find_element(By.CSS_SELECTOR, '.promo-media picture img')
                image_file_name = image.get_attribute('src')
            except:
                image_file_name = None
            try:
                urllib.request.urlretrieve(image_file_name, file_path)
                time.sleep(2)
            except:
                1 == 1
            money_on_text = contains_money_on_text(title,description)
            times_search_term_appears = count_ocurrences(search_term,title, description)
            temp_article = Article(title,publich_date,description,image_file_name, money_on_text,times_search_term_appears)
            article_list.append(temp_article)
        try:
            driver.find_element(By.CLASS_NAME, 'search-results-module-next-page').click()
        except:
            break
        time.sleep(3)
    driver.quit()
    return article_list
