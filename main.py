from database import create_tables
from crawler import get_event_data
from crawler.crawler import Crawler
from database.models import add_locations, add_events, add_works, add_dates, add_date_events_table, add_artists, \
    add_event_artists_table, add_tickets, add_event_tickets_table

if __name__ == '__main__':
    crawler = Crawler()
    events_soup = crawler.get_soup(url="https://www.lucernefestival.ch/en/program/summer-festival-23")
    links = crawler.get_links(events_soup, tag_="div", class_="cell shrink show-for-large")
    #
    data = [get_event_data(links[i], crawler) for i in range(0, len(links)) if i == 0][0]

    # create_tables()
    # # Adding Event Location to the database
    # add_locations(data)
    # add_events(data)
    # add_works(data)
    # add_dates(data)
    # add_date_events_table(data)
    # add_artists(data)
    # add_event_artists_table(data)
    # add_tickets(data)
    add_event_tickets_table(data)