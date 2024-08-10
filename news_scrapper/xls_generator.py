import pandas as pd
import news_scraping
from datetime import datetime

found_articles = news_scraping.la_news_scrapper('Brazil', '', 3)
data_frame = pd.DataFrame([vars(article) for article in found_articles])
data_frame.rename(columns={'publich_date':'date', 'picture_file_name':'picture filename',
        'times_search_term_appears':'count of search phrases in the title and description'}, inplace= True)
file_name = 'scrapped_articles_' + datetime.now().strftime("%m-%d-%Y %H:%M:%S").replace(" ", "_") + '.xlsx'
data_frame.to_excel(file_name, index=False)
