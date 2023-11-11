import pandas as pd
import mysql.connector

#MySQL database credentials
host = "localhost"
user = "root"
password = "9618233565"
database = "INVSTO"
table = "stock_data"
# CSV file path
csv_file = r"C:\Users\aagar\PycharmProjects\invsto\HINDALCO.csv"

try:
    # Establishing connection.
    conn = mysql.connector.connect(
        host=host,
        user=user,
        password=password,
        database=database
    )
    if conn.is_connected():
        print("Connected to MySQL database, Entering data.")
        # Create a cursor object to interact with the database
        cursor = conn.cursor()
        # Read the CSV file into a DataFrame
        df = pd.read_csv(csv_file, sep=',')  # Assuming tab-separated values

        # Insert data from the DataFrame into the MySQL table
        for index, row in df.iterrows():
            # Extract instrument values as a list
            instruments = row['instrument'].split(',')

            # Remove leading and trailing whitespaces from each instrument
            instruments = [i.strip() for i in instruments]

            # Create a tuple for the values to be inserted
            data_to_insert = (
                row['datetime'], row['close'], row['high'], row['low'],
                row['open'], row['volume'], ','.join(instruments)
            )
            # Insert data into the MySQL table
            insert_query = f"INSERT INTO {table} (datetime, close, high, low, open, volume, instrument) VALUES (%s, %s, %s, %s, %s, %s, %s)"
            cursor.execute(insert_query, data_to_insert)
        # Committing the changes to the database
        conn.commit()
        print(f"Data inserted from the CSV file into the table: {table}")

#error handling.
except mysql.connector.Error as e:
    print(f"Error: {e}")
finally:
    # Close the cursor and connection
    if 'cursor' in locals():
        cursor.close()
    if 'conn' in locals() and conn.is_connected():
        conn.close()
        print("MySQL connection closed.Thank You")