from crawler import crawler
from database import db
from database_utils import insert_data_to_postgres
from plotter.plotter import get_events_per_day

if __name__ == '__main__':
    events_soup = crawler.get_soup(url="https://www.lucernefestival.ch/en/program/summer-festival-23")
    links = crawler.get_links(events_soup, tag_="div", class_="cell shrink show-for-large")

    # db.create_tables()

    """
    Inserts data in the database, the active parameter is for running the function or not, if data is already
    in place, this can be set to False.
    The add to db methods, have constrains to avoid adding duplicates, keep in mind some info can be reused such as
    dates, locations, etc.
    """
    insert_data_to_postgres(links=links, crawler=crawler, active=False)

    get_events_per_day()



