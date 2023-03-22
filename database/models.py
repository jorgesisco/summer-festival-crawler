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
    date TIMESTAMP NOT NULL
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
    price INTEGER NOT NULL
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
        date_time_str = f"{current_year}-{date_string.replace('.', '-')} {time_string.replace('.', ':')}:00"

        # print(date_time_str)
        # Checking if date data is added already
        select_query = "SELECT date FROM dates WHERE date = %s"

        cursor.execute(select_query, (date_time_str,))
        existing_date = cursor.fetchone()

        insert_query = "INSERT INTO dates (date) VALUES (%s)"

        if existing_date is None:

            cursor.execute(insert_query, (date_time_str,))
            conn.commit()
            print("Date added to the dates table!")

        else:
            print("Date already exists in the dates table")

        cursor.close()
        conn.close()

    except psycopg2.Error as error:
        print(f"Error: {error}")
