from robocorp.tasks import task
from output.news_scrapper import news_scraping, xls_generator
import json
import os

@task
def solve_challenge():
    """
    * Parameters
    The process must process three parameters via the robocluod work item
    search phrase, news category/section/topic, number of months for which you 
    need to receive news (if applicable),
    Example of how this should work: 0 or 1 - only the current month,
      2 - current and previous month, 3 - current and two previous months, and so on

    These may be defined within a configuration file, but we’d prefer they be provided 
    via a Robocloud workitem
    * The Process
    The main steps:

    Open the site by following the link
    Enter a phrase in the search field
    On the result page
    If possible select a news category or section from the
    Choose the latest (i.e., newest) news
    Get the values: title, date, and description.

    Store in an Excel file:
        title
        date
        description (if available)
        picture filename
        count of search phrases in the title and description
        True or False, depending on whether the title or description contains any amount of money
            Possible formats: $11.1 | $111,111.11 | 11 dollars | 11 USD

    Download the news picture and specify the file name in the Excel file
    Follow steps 4-6 for all news that falls within the required time period
    """
    with open("output/config.json") as config_file:
        config = json.load(config_file)

    config['search_term'] = os.getenv('search_term', config.get('search_term'))
    config['select_topic'] = os.getenv('select_topic', config.get('select_topic'))
    config['months'] = os.getenv('months', config.get('months'))

    try:
        articles_list = news_scraping.la_news_scrapper(config['search_term'],config['select_topic'], config['months'])
        xls_generator.generate_xlsx_from_articles(articles_list)
    finally:
        # A place for teardown and cleanups. (Playwright handles browser closing)
        print("Automation finished!")
