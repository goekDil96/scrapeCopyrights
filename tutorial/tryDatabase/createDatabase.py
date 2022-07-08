import psycopg2
import mysql.connector

def main():
    # establishing the connection
    conn = psycopg2.connect(database="postgres", user="postgres", host="127.0.0.1", port="5432")

    # Creating a curser object using the cursor() method
    cursor = conn.curser()

    # Preparing query to create a database
    sql = """CREATE database mydb;"""

    # creating a database
    cursor.execute(sql)
    print("Database created sucessfully...................")


if __name__ == "__main__":
    main()