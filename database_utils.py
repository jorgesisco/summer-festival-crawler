from crawler import get_event_data
from database import db


def insert_data_to_postgres(links, crawler, active):

    if active is True:
        for link in links:
            data = get_event_data(link, crawler)

            """
            Added this condition for one event that has no venue info, I can always add additinoal constrains to the
            models.py so I can still add event with an empty loation row, to avoid messing with the squema.
            """
            if data['event_venue']:

                db.add_locations(data)
                db.add_events(data)
                db.add_works(data)
                db.add_dates(data)
                db.add_date_events_table(data)
                db.add_artists(data)
                db.add_event_artists_table(data)
                db.add_tickets(data)
                db.add_event_tickets_table(data)

            else:
                print("Event ignored since is missing Venue info including address")

        return

    else:
        return

