import re
from datetime import datetime
import psycopg2

# Replace with your PostgreSQL database connection information
# DATABASE_URL = "postgresql://admin:admin@db:5432/database" \
#                ""

DATABASE_URL = "postgresql://admin:admin@db:5432/database"

# SQL commands to create the tables
create_locations_table = """
CREATE TABLE locations (
    id SERIAL PRIMARY KEY,
    name VARCHAR(500) NOT NULL,
    address VARCHAR(500) NOT NULL,
    address_url VARCHAR(500) NOT NULL,
    city VARCHAR(50) NOT NULL,
    country VARCHAR(50) NOT NULL,
    description VARCHAR(2000) NOT NULL,
    arriving_bus_train VARCHAR(500) NOT NULL,
    arriving_auto VARCHAR(500) NOT NULL,
    p_rail VARCHAR(500) NOT NULL,
    flights_info VARCHAR(500) NOT NULL,
    concierge VARCHAR(500) NOT NULL,
    cloakroom VARCHAR(500) NOT NULL,
    wheelchair_sitting VARCHAR(2000) NOT NULL,
    late_admissions VARCHAR(2000) NOT NULL,
    gastronomy VARCHAR(500) NOT NULL

);
"""

create_events_table = """
CREATE TABLE events (
    id SERIAL PRIMARY KEY,
    location_id INTEGER REFERENCES locations (id),
    title VARCHAR(1000) NOT NULL,
    description VARCHAR(2000) NOT NULL,
    envent_url VARCHAR(500),
    image_url VARCHAR(500)
);

"""

create_works_table = """
CREATE TABLE works (
    id SERIAL PRIMARY KEY,
    event_id INTEGER REFERENCES events (id),
    work_program VARCHAR(50) NOT NULL,
    works TEXT[] NOT NULL,
    work_author TEXT[] NOT NULL
);

"""

create_artists_table = """
CREATE TABLE artists (
    id SERIAL PRIMARY KEY,
    name VARCHAR(50) NOT NULL
);

"""

create_event_artists_table = """
CREATE TABLE event_artists (
    event_id INTEGER REFERENCES events (id),
    artist_id INTEGER REFERENCES artists (id)
);

"""

create_dates_table = """
CREATE TABLE dates (
    id SERIAL PRIMARY KEY,
    date DATE NOT NULL,
    time TIME NOT NULL
);
"""

create_events_date = """
CREATE TABLE event_dates (
    event_id INTEGER REFERENCES events (id),
    date_id INTEGER REFERENCES dates (id)
);
"""

create_tickets = """
CREATE TABLE tickets (
    id SERIAL PRIMARY KEY,
    price INTEGER NOT NULL,
    currency VARCHAR(10) NOT NULL
);

"""

create_event_tickets = """
CREATE TABLE event_tickets (
    event_id INTEGER REFERENCES events (id),
    ticket_id INTEGER REFERENCES tickets (id)
);

"""


# Connect to the database and create the tables
def create_tables():
    try:
        conn = psycopg2.connect(DATABASE_URL)
        cursor = conn.cursor()

        # Check if tables already exist
        tables = ['locations', 'events', 'works', 'artists', 'event_artists',
                  'dates', 'events_dates', 'tickets', 'event_tickets']

        existing_tables = []
        for table in tables:
            cursor.execute(
                f"SELECT EXISTS(SELECT 1 FROM pg_catalog.pg_tables WHERE schemaname='public' AND tablename='{table}');")
            result = cursor.fetchone()[0]
            if result:
                existing_tables.append(table)

        if existing_tables:
            print(f"The following tables already exist: {existing_tables}")
            return

        cursor.execute(create_locations_table)
        cursor.execute(create_events_table)
        cursor.execute(create_works_table)
        cursor.execute(create_artists_table)
        cursor.execute(create_event_artists_table)
        cursor.execute(create_dates_table)
        cursor.execute(create_events_date)
        cursor.execute(create_tickets)
        cursor.execute(create_event_tickets)
        conn.commit()
        cursor.close()
        conn.close()

        print("Tables created successfully!")
    except psycopg2.Error as error:
        print(f"Error: {error}")


def add_locations(data):
    try:
        conn = psycopg2.connect(DATABASE_URL)
        cursor = conn.cursor()

        insert_query = "INSERT INTO locations (name, address, address_url, city, country, description, arriving_bus_train, arriving_auto, p_rail, flights_info, concierge, cloakroom, wheelchair_sitting, late_admissions, gastronomy) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"

        city = re.findall(r'\b\w+\b', data['event_venue']['address'])[-1]
        country = 'Switzerland'

        # Check if the primary key already exists with the data before adding to the table
        select_query = "SELECT * FROM locations WHERE name = %s AND address = %s"
        cursor.execute(select_query, (data['event_venue']['venue'], data['event_venue']['address']))
        row = cursor.fetchone()

        if row is None:
            cursor.execute(insert_query, (
                data['event_venue']['venue'], data['event_venue']['address'],
                data['event_venue']['address_url'],
                city, country, data['description'],
                data['event_venue']['arriving_bus_train'], data['event_venue']['arriving_auto'],
                data['event_venue']['p_rail'], data['event_venue']['flights_info'],
                data['event_venue']['concierge_info'],
                data['event_venue']['cloakroom'], data['event_venue']['wheelchair_sitting'],
                data['event_venue']['late_admissions'], data['event_venue']['restaurants_info']))
            conn.commit()
            print("Data added to location table!")

        else:
            # Primary key already exists, so skip the insertion
            print("Data already exists in the locations table")

        cursor.close()
        conn.close()


    except psycopg2.Error as error:
        print(f"Error: {error}")


def add_events(data):
    try:
        conn = psycopg2.connect(DATABASE_URL)
        cursor = conn.cursor()

        # Querying location row to get id
        location_query = "SELECT * FROM locations WHERE address = %s"
        location_address = (data['event_venue']['address'],)
        cursor.execute(location_query, location_address)
        location_row = cursor.fetchone()

        # Checking if event data is already in the events table
        select_query = "SELECT * FROM events WHERE title = %s AND description = %s"
        cursor.execute(select_query, (data['title'], data['description']))
        row = cursor.fetchone()

        insert_query = "INSERT INTO events (location_id, title, description, envent_url, image_url) VALUES (%s, %s, %s, %s, %s)"

        if location_row is not None:
            if row is None:
                location_id = location_row[0]
                cursor.execute(insert_query,
                               (location_id, data['title'], data['description'], data['link'], data['image_link']))
                conn.commit()
                print("Data added to the events table!")

            else:
                # Primary key already exists, so skip the insertion
                print("Data already exists in the events table")
        else:
            print('Could not find location in he locations table')

        cursor.close()
        conn.close()

    except psycopg2.Error as error:
        print(f"Error: {error}")

        # currently working on adding event data along with the location id from other table


def add_works(data):
    try:
        conn = psycopg2.connect(DATABASE_URL)
        cursor = conn.cursor()

        # Querying events row to get id
        event_query = "SELECT * FROM events WHERE title = %s AND description = %s"
        event_address = (data['title'], data['description'],)
        cursor.execute(event_query, event_address)
        event_row = cursor.fetchone()
        event_id = event_row[0]

        # Checking if work data is added already
        select_query = "SELECT * FROM works WHERE event_id = %s"
        cursor.execute(select_query, (event_id,))
        row = cursor.fetchone()

        insert_query = "INSERT INTO works (event_id, work_program, works, work_author) VALUES (%s, %s, %s, %s)"

        if event_row is not None:
            if row is None:
                cursor.execute(insert_query,
                               (
                                   event_id, data['works']['program'], data['works']['work'],
                                   data['works']['work_author']))
                conn.commit()
                print("Data added to the works table!")

            else:
                # Primary key already exists, so skip the insertion
                print("Data already exists in the works table")
        else:
            print('Could not find event in he events table')

        cursor.close()
        conn.close()

    except psycopg2.Error as error:
        print(f"Error: {error}")


def add_dates(data):
    try:
        conn = psycopg2.connect(DATABASE_URL)
        cursor = conn.cursor()

        current_year = datetime.now().year
        date_string = data['date']
        time_string = data['time']

        """
        Defining year, since the website does not show the year, here I am checking if the shown month 
        if smaller than current month, if it is, then the year set will be next year.
        """
        if int(date_string[:2]) < datetime.now().month:
            date_str = f"{current_year+1}-{date_string.replace('.', '-')}"
        else:
            date_str = f"{current_year}-{date_string.replace('.', '-')}"

        time_str = f"{time_string.replace('.', ':')}:00"

        # print(date_time_str)
        # Checking if date data is added already
        select_query = "SELECT date FROM dates WHERE date = %s and time = %s"

        cursor.execute(select_query, (date_str, time_str))
        existing_date = cursor.fetchone()

        insert_query = "INSERT INTO dates (date, time) VALUES (%s, %s)"

        if existing_date is None:

            cursor.execute(insert_query, (date_str, time_str))
            conn.commit()
            print("Date and time added to the dates table!")

        else:
            print("Date and time already exists in the dates table")

        cursor.close()
        conn.close()

    except psycopg2.Error as error:
        print(f"Error: {error}")


def add_date_events_table(data):
    try:
        conn = psycopg2.connect(DATABASE_URL)
        cursor = conn.cursor()

        current_year = datetime.now().year
        date_string = data['date']
        time_string = data['time']
        date_time_str = f"{current_year}-{date_string.replace('.', '-')} {time_string.replace('.', ':')}:00"

        # Querying events row to get id
        event_query = "SELECT * FROM events WHERE title = %s AND description = %s"
        event_address = (data['title'], data['description'],)
        cursor.execute(event_query, event_address)
        event_row = cursor.fetchone()
        event_id = event_row[0]

        # Querying date row to get id
        date_query = "SELECT * FROM dates WHERE date = %s"
        date_data = (date_time_str,)
        cursor.execute(date_query, date_data)
        date_row = cursor.fetchone()
        date_id = date_row[0]

        # Checking if work data is added already
        select_query = "SELECT * FROM event_dates WHERE event_id = %s and date_id = %s"
        cursor.execute(select_query, (event_id, date_id))
        row = cursor.fetchone()

        insert_query = "INSERT INTO event_dates (event_id, date_id) VALUES (%s, %s)"

        if event_row and date_row:
            if row is None:
                cursor.execute(insert_query, (event_id, date_id))
                conn.commit()
                print("event_id and date_id added to the event_dates table!")

            else:
                # Primary key already exists, so skip the insertion
                print("event_id and date_id already exists in the event_dates table")
        else:
            print('Could not find event_id and date_id in he event_dates table')

        cursor.close()
        conn.close()

    except psycopg2.Error as error:
        print(f"Error: {error}")


def add_artists(data):
    try:
        conn = psycopg2.connect(DATABASE_URL)
        cursor = conn.cursor()

        # Checking if artist data is added already
        for artist in data['performers']:
            select_query = "SELECT name FROM artists WHERE name = %s"
            cursor.execute(select_query, (artist,))
            existing_artist = cursor.fetchone()

            insert_query = "INSERT INTO artists (name) VALUES (%s)"

            if existing_artist is None:

                cursor.execute(insert_query, (artist,))
                conn.commit()
                print("Artist name added to the dates table!")

            else:
                print("Artist already exists in the artists table")

        cursor.close()
        conn.close()

    except psycopg2.Error as error:
        print(f"Error: {error}")


def add_event_artists_table(data):
    try:
        conn = psycopg2.connect(DATABASE_URL)
        cursor = conn.cursor()

        # Querying events row to get id
        event_query = "SELECT * FROM events WHERE title = %s AND description = %s"
        event_address = (data['title'], data['description'],)
        cursor.execute(event_query, event_address)
        event_row = cursor.fetchone()
        event_id = event_row[0]

        for artist in data['performers']:
            # Querying artists rows to get ids
            artist_query = "SELECT * FROM artists WHERE name = %s"
            artist_data = (artist,)
            cursor.execute(artist_query, artist_data)
            artist_row = cursor.fetchone()
            artist_id = artist_row[0]

            # Checking if artist_event data is added already
            select_query = "SELECT * FROM event_artists WHERE event_id = %s AND artist_id = %s"
            cursor.execute(select_query, (event_id, artist_id))
            existing_artist = cursor.fetchone()

            insert_query = "INSERT INTO event_artists (event_id, artist_id) VALUES (%s, %s)"

            if event_row or artist_row:
                if existing_artist is None:
                    cursor.execute(insert_query, (event_id, artist_id))
                    conn.commit()
                    print("event_id and artist_id added to the event_artists table!")

                else:
                    print("event_id and artist_id already exists in the event_artists table")

            else:
                print('Could not find event_id or artist_id in he event_artists table')

        cursor.close()
        conn.close()

    except psycopg2.Error as error:
        print(f"Error: {error}")


def add_tickets(data):
    try:
        conn = psycopg2.connect(DATABASE_URL)
        cursor = conn.cursor()

        price = data['ticket_price']
        price_int = [int(x) for x in re.findall(r'\d+', price)][0]

        currency = ''.join(re.findall(r'\D+', price))
        # Checking if ticket data is added already
        select_query = "SELECT price FROM tickets WHERE price = %s"
        cursor.execute(select_query, (price_int,))
        existing_price = cursor.fetchone()

        insert_query = "INSERT INTO tickets (price, currency) VALUES (%s, %s)"

        if existing_price is None:
            cursor.execute(insert_query, (price_int, currency))
            conn.commit()
            print("Price and currency added to the tickets table!")

        else:
            print("Price already exists in the tickets table")

        cursor.close()
        conn.close()

    except psycopg2.Error as error:
        print(f"Error: {error}")


def add_event_tickets_table(data):
    try:
        conn = psycopg2.connect(DATABASE_URL)
        cursor = conn.cursor()

        # Querying events row to get id
        event_query = "SELECT * FROM events WHERE title = %s AND description = %s"
        event_data = (data['title'], data['description'],)
        cursor.execute(event_query, event_data)
        event_row = cursor.fetchone()
        event_id = event_row[0]

        price = data['ticket_price']
        price_int = [int(x) for x in re.findall(r'\d+', price)][0]

        # Querying tickets row to get id
        ticket_query = "SELECT * FROM tickets WHERE price = %s"
        ticket_data = (price_int,)
        cursor.execute(ticket_query, ticket_data)
        ticket_row = cursor.fetchone()
        ticket_id = ticket_row[0]

        # Checking if event_tickets data is added already
        select_query = "SELECT * FROM event_tickets WHERE event_id = %s and ticket_id = %s"
        cursor.execute(select_query, (event_id, ticket_id))
        row = cursor.fetchone()

        insert_query = "INSERT INTO event_tickets (event_id, ticket_id) VALUES (%s, %s)"

        if event_row and ticket_row:
            if row is None:
                cursor.execute(insert_query, (event_id, ticket_id))
                conn.commit()
                print("event_id and ticket_id added to the event_tickets table!")

            else:
                # Primary key already exists, so skip the insertion
                print("event_id and ticket_id already exists in the event_tickets table")
        else:
            print('Could not find event_id and ticket_id in he event_tickets table')

        cursor.close()
        conn.close()

    except psycopg2.Error as error:
        print(f"Error: {error}")