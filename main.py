from database import create_tables
from crawler import get_event_data
from crawler.crawler import Crawler
from database.models import add_locations, add_events

if __name__ == '__main__':
    create_tables()

    crawler = Crawler()
    events_soup = crawler.get_soup(url="https://www.lucernefestival.ch/en/program/summer-festival-23")
    links = crawler.get_links(events_soup, tag_="div", class_="cell shrink show-for-large")
    #
    data = [get_event_data(links[i], crawler) for i in range(0, len(links)) if i == 0][0]
    # #
    # # Adding Event Location to the database
    add_locations(data)
    add_events(data)
