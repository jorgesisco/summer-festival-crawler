import psycopg2
from matplotlib import pyplot as plt
from database import db


def get_events_per_day():
    # conn = db.db_connect()

    dsn = "dbname=database user=admin password=admin host=localhost port=5432"
    conn = psycopg2.connect(dsn)
    # conn = psycopg2.connect("postgresql://admin:admin@db:5432/database")

    cur = conn.cursor()

    query = """
                SELECT dates.date, COUNT(events.id) AS event_count
                FROM dates
                JOIN event_dates ON dates.id = event_dates.date_id
                JOIN events ON event_dates.event_id = events.id
                GROUP BY dates.date
                ORDER BY dates.date;
            """

    cur.execute(query)
    results = cur.fetchall()

    # Convert the results to two separate lists of dates and event counts
    dates = [result[0] for result in results]
    event_counts = [result[1] for result in results]

    # Create a bar plot of the events per date using Matplotlib
    plt.bar(dates, event_counts)
    plt.xlabel('Date')
    plt.ylabel('Number of Events')
    plt.title('Events per Date')
    plt.show()
    # Close the cursor and connection to the database
    cur.close()
    conn.close()