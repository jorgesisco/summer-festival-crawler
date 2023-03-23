import psycopg2
from matplotlib import pyplot as plt


def get_events_per_day(active):
    """
        Retrieves the number of events per day from a Postgres database and creates a bar plot using Matplotlib.

        The function connects to a Postgres database using hardcoded credentials, and executes a query to count the number
        of events for each day in the database. The results are then plotted using Matplotlib.

        Parameters:
        None.

        Returns:
        None.
        """

    if active:
        dsn = "dbname=database user=admin password=admin host=localhost port=5432"
        conn = psycopg2.connect(dsn)

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

        """Convert the results to two separate lists of dates and event counts"""
        dates = [result[0] for result in results]
        event_counts = [result[1] for result in results]

        """Create a bar plot of the events per date using Matplotlib"""
        plt.bar(dates, event_counts)
        plt.xlabel('Date')
        plt.ylabel('Number of Events')
        plt.title('Events per Date')
        plt.show()

        """Close the cursor and connection to the database"""
        cur.close()
        conn.close()

    else:
        return
