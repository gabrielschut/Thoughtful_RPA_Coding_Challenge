from robocorp.tasks import task
from output.news_scrapper import news_scraping, xls_generator


@task
def solve_challenge():
    """
    Main task which solves the RPA challenge!

    Downloads the source data Excel file and uses Playwright to fill the entries inside
    rpachallenge.com.
    """
    try:
        articles_list = news_scraping.la_news_scrapper('dollars', 'Hollywood Inc.', 5)
        xls_generator.generate_xlsx_from_articles(articles_list)
    finally:
        # A place for teardown and cleanups. (Playwright handles browser closing)
        print("Automation finished!")
