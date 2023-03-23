from crawler import crawler
from database import db
from database_utils import insert_data_to_postgres
from plotter.plotter import get_events_per_day

if __name__ == '__main__':
    """
    Using Crawler instance get_links to retrieve a list with event links
    """
    events_soup = crawler.get_soup(url="https://www.lucernefestival.ch/en/program/summer-festival-23")
    links = crawler.get_links(events_soup, tag_="div", class_="cell shrink show-for-large")

    """
    Running DataBase to create tables, if they exist already, the code won't run
    """
    db.create_tables()

    """
    Running function to insert data in the database, the active parameter is for running the function or not, if data is already
    in the database, this can be set to False.
    """
    insert_data_to_postgres(links=links, crawler=crawler, active=False)

    get_events_per_day()



