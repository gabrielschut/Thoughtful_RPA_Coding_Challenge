import pandas as pd
from datetime import datetime
import os

def generate_xlsx_from_articles(articles_list):
        data_frame = pd.DataFrame([vars(article) for article in articles_list])
        data_frame.rename(columns={'publich_date':'date', 'picture_file_name':'picture filename',
                'times_search_term_appears':'count of search phrases in the title and description'}, inplace= True)
        file_name = 'scrapped_articles_' + datetime.now().strftime("%m-%d-%Y %H:%M:%S").replace(" ", "_") + '.xlsx'
        directory = "output/xls_files/"
        if not os.path.exists(directory):
                os.makedirs(directory)
        data_frame.to_excel(f'{directory}{file_name}', index=False)
