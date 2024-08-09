import pandas as pd
import news_scraping


found_articles = news_scraping.la_news_scrapper('Gold', 'California', 5)
data_frame = pd.DataFrame([vars(article) for article in found_articles])
data_frame.rename(columns={'publich_date':'date', 'picture_file_name':'picture filename',
        'times_search_term_appears':'count of search phrases in the title and description'}, inplace= True)

data_frame.to_excel('scrapped_articles.xlsx', index=False)
