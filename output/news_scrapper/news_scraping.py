import time
from datetime import date
import re

from RPA.Browser.Selenium import Selenium
from selenium.webdriver.common.keys import Keys

from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select

from output.news_scrapper.utils import last_date, file_maneger
from output.news_scrapper.article import Article


def contains_money_on_text(title, description):
        pattern = r'\$\d{1,3}(,\d{3})*(\.\d{1,2})?|(\d{1,3}(,\d{3})*(\.\d{1,2})? (dollars|USD))'
        # Compiles the regex with the ignore whitespace options
        regex = re.compile(pattern, re.VERBOSE | re.IGNORECASE)
        if (regex.search(title) or regex.search(description)):
            return True
        return False


def count_ocurrences(search_phrase : str, title : str, description : str):
    ocorrences = title.lower().count(search_phrase.lower())
    ocorrences += description.lower().count(search_phrase.lower())
    return ocorrences


def la_news_scrapper(search_term ,select_topic, months):
    browser = Selenium() 
    article_list = []
    browser.open_available_browser('https://www.latimes.com/', headless= True)
    browser.driver.maximize_window()
    browser.click_button("//button[@data-element='search-button']")
    time.sleep(3)
    browser.input_text("//input[@data-element='search-form-input']", search_term)
    browser.input_text("//input[@data-element='search-form-input']", Keys.ENTER, False)
    time.sleep(5)
    browser.click_button("//button[@class='button see-all-button']")
    time.sleep(3)
    topics = browser.driver.find_elements(By.CLASS_NAME, 'checkbox-input-label')
    if (not select_topic == '' or select_topic == None):
        for topic in topics:
            if (topic.text == select_topic):
                topic.click()
                break
    time.sleep(3)
    select_element = browser.driver.find_element(By.CSS_SELECTOR, '.search-results-module-sorts .select-input')
    select = Select(select_element)
    select.select_by_visible_text('Newest') 
    time.sleep(3)
    next_page = True
    while next_page:
        articles = []
        articles = browser.driver.find_elements(By.CLASS_NAME, 'promo-wrapper')
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
            if(image_file_name != None or image_file_name != ' ' or image_file_name != ''):
                try:
                    parts = image_file_name.rsplit('https', 1)
                    file_name = parts[-1][3:] if len(parts) > 1 else image_file_name
                    file_maneger.download_image(image_file_name,file_name)
                    image_file_name = file_name
                    time.sleep(2)
                except:
                    1 == 1
            money_on_text = contains_money_on_text(title,description)
            times_search_term_appears = count_ocurrences(search_term,title, description)
            temp_article = Article(title,publich_date,description,image_file_name, money_on_text,times_search_term_appears)
            article_list.append(temp_article)
        try:
            browser.driver.find_element(By.CLASS_NAME, 'search-results-module-next-page').click()
        except:
            break
        time.sleep(3)
    browser.driver.quit()
    return article_list
