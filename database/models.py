import re

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
    title VARCHAR(255) NOT NULL,
    description TEXT NOT NULL,
    envent_url VARCHAR(255),
    image_url VARCHAR(255)
);

"""

create_works_table = """
CREATE TABLE works (
    id SERIAL PRIMARY KEY,
    event_id INTEGER REFERENCES events (id),
    work_title VARCHAR(255) NOT NULL
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

        # Check if the primary key already exists in the table
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
            print("Data already exists in the table")

        cursor.close()
        conn.close()


    except psycopg2.Error as error:
        print(f"Error: {error}")

def add_events(data, link):
    try:
        conn = psycopg2.connect(DATABASE_URL)
        cursor = conn.cursor()

        row = cursor.execute("SELECT * FROM locations WHERE address = %s", (data['event_venue']['address'],))

        # insert_query = "INSERT INTO events (location_id, title, description, event_link, image_link,) VALUES (%s, %s, %s, %s, %s)"

        if row is not None:
            location_id = row[0]
            print(location_id)
            # cursor.execute(insert_query, (location_id, data['title'], data['description'], link,  ))

    except psycopg2.Error as error:
        print(f"Error: {error}")

        #currently working on adding event data along with the location id from other table