import psycopg2
import argparse
import time
from datetime import datetime, timedelta

def fetch_data(database_host, database_port, database_name, database_table_name, database_username, database_password):
    try:
        # connect to PostgreSQL database
        with psycopg2.connect(
            dbname=database_name,
            user=database_username,
            password=database_password,
            host=database_host,
            port=database_port
        ) as conn:
            print(f"Connected to table {database_table_name} in database {database_name} at {database_host}:{database_port} as {database_username}")

            # create cursor
            with conn.cursor() as cur:
                # fetch data from database and print
                while True:
                    cur.execute(f"SELECT * FROM {database_table_name} ORDER BY window_start DESC LIMIT 60")
                    rows = cur.fetchall()

                    print("ADDED DATA->time_window \t title(film_id) \t scores_sum \t scores_count \t unique_scores_count")
                    for row in rows:
                        win_start = datetime.utcfromtimestamp(row[0]).strftime('%Y-%m-%d')
                        win_end = (datetime.utcfromtimestamp(row[0]) + timedelta(days=30)).strftime('%Y-%m-%d')
                        film_id = row[1]
                        title = row[2]
                        scores_sum = row[3]
                        scores_count = row[4]
                        unique_scores_count = row[5]
                        print(f"{win_start} - {win_end} \t {title}({film_id}) \t {scores_sum} \t {scores_count} \t {unique_scores_count}")
                    time.sleep(15)

    except psycopg2.Error as e:
        print("Error: Connection to database failed")
        print(e)

def main():
    parser = argparse.ArgumentParser(description="Fetch data from PostgreSQL database")
    parser.add_argument("database_host", help="Host address of the database")
    parser.add_argument("database_port", help="Port number of the database")
    parser.add_argument("database_name", help="Name of the database")
    parser.add_argument("database_table_name", help="Name of the database tablr")
    parser.add_argument("database_username", help="Username for accessing the database")
    parser.add_argument("database_password", help="Password for accessing the database")
    args = parser.parse_args()

    fetch_data(args.database_host, args.database_port, args.database_name, args.database_table_name, args.database_username, args.database_password)

if __name__ == "__main__":
    main()