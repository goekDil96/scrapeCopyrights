import psycopg2
import os
from dotenv import load_dotenv

load_dotenv("config/.env")

## class source:
# 0: original dataset
# 1: generated data
# 3: scraped data

DATABASE = str(os.getenv("DATABASE"))
HOST = str(os.getenv("HOST"))
PORT = int(os.getenv("PORT"))
USER = str(os.getenv("USER"))
PASSWORD = str(os.getenv("PASSWORD"))

class ManageDatabase():
    def __init__(self,
                 database: str = DATABASE,
                 host: str = HOST,
                 port: int = PORT,
                 user: str = USER,
                 password: str = PASSWORD
                 ):
        
        self.host = host
        self.port = port
        self.user = user
        self.password = password
        self.database = database
        
    @property
    def host(self):
        return self.__host

    @host.setter
    def host(self, value: str):
        if type(value) != str:
            raise ValueError
        self.__host = value

    @property
    def port(self):
        return self.__port

    @port.setter
    def port(self, value: int):
        if type(value) != int:
            raise ValueError
        self.__port = value

    @property
    def user(self):
        return self.__user

    @user.setter
    def user(self, value: str):
        if type(value) != str:
            raise ValueError
        self.__user = value
    
    @property
    def password(self):
        return self.__password

    @password.setter
    def password(self, value: str):
        if type(value) != str:
            raise ValueError
        self.__password = value
    
    @property
    def database(self):
        return self.__database

    @database.setter
    def database(self, value: str):
        self.__database = value
        try:
            # check if database already exists
            conn = psycopg2.connect(database=self.__database,
                                    user=self.__user,
                                    password=self.__password,
                                    host=self.__host,
                                    port=self.__port)
            
            print("Database already exists...................")

        except:
            ## Step 1: Create Database
            conn = psycopg2.connect(user=self.__user,
                                    password=self.__password,
                                    port=self.__port,
                                    host=self.__host)
            conn.autocommit = True

            # Creating a curser object using the cursor() method
            cursor = conn.cursor()

            # Preparing query to create a database
            sql = f"""CREATE database {self.__database};"""

            # creating a database
            cursor.execute(sql)
            print("Database created sucessfully...................")
        
        finally:
            conn = psycopg2.connect(database=self.__database,
                                    user=self.__user,
                                    password=self.__password,
                                    host=self.__host,
                                    port=self.__port)

            # Creating a curser object using the cursor() method
            cursor = conn.cursor()

            # Preparing query to create a database
            sql = """CREATE TABLE IF NOT EXISTS COPYRIGHTS(
                COPYRIGHT_STRING VARCHAR(500) NOT NULL UNIQUE,
                COPYRIGHT_CLASSIFICATION INT,
                COPYRIGHT_SOURCE INT
                );"""
            
            cursor.execute(sql)
            conn.commit()

            conn.close()

    def create_entry(self, *, 
                     COPYRIGHT_STRING: str,
                     COPYRIGHT_CLASSIFICATION: str or None=None,
                     COPYRIGHT_SOURCE: str or None=None
                     ) -> bool:
        response = False
        for i, j, k in [(COPYRIGHT_CLASSIFICATION, int, None), (COPYRIGHT_SOURCE, int, None), (COPYRIGHT_STRING, str, str)]:
            if type(i) != j and type(i) != k and type(i) != type(k):
                print(j)
                raise ValueError
        try:
            # establishing the connection
            conn = psycopg2.connect(database=self.__database,
                                    user=self.__user,
                                    password=self.__password,
                                    host=self.__host,
                                    port=self.__port)

            # Creating a curser object using the cursor() method
            cursor = conn.cursor()


            tablehead = "COPYRIGHT_STRING"
            if COPYRIGHT_CLASSIFICATION:
                tablehead += ", COPYRIGHT_CLASSIFICATION"
            if COPYRIGHT_SOURCE:
                tablehead += ", COPYRIGHT_SOURCE"

            tablebody = f"'{COPYRIGHT_STRING}'"
            if COPYRIGHT_CLASSIFICATION:
                tablebody += f", {COPYRIGHT_CLASSIFICATION}"
            if COPYRIGHT_SOURCE:
                tablebody += f", {COPYRIGHT_SOURCE}"

            # Preparing query to create a database
            sql = f"""INSERT INTO COPYRIGHTS({tablehead})
                    VALUES ({tablebody});"""
            
            cursor.execute(sql)
            conn.commit()
            response = True
        except (Exception, psycopg2.DatabaseError) as error:
            print(error)
        finally:
            conn.close()
            return response

    def update_entry(self, *,
                     COPYRIGHT_STRING: str,
                     COPYRIGHT_CLASSIFICATION: str or None=None,
                     COPYRIGHT_SOURCE:str or None=None) -> bool:

        for i, j, k in [(COPYRIGHT_CLASSIFICATION, int, None), (COPYRIGHT_SOURCE, int, None), (COPYRIGHT_STRING, str, str)]:
            if type(i) != j and type(i) != k and type(i) != type(k):
                print(type(i))
                raise ValueError
        # establishing the connection
        conn = psycopg2.connect(database=self.__database,
                                user=self.__user,
                                password=self.__password,
                                host=self.__host,
                                port=self.__port)

        # Creating a curser object using the cursor() method
        cursor = conn.cursor()
        conn.autocommit = True

        if COPYRIGHT_CLASSIFICATION:
            # Preparing query to create a database
            sql = f"""UPDATE COPYRIGHTS
                    SET COPYRIGHT_CLASSIFICATION = {COPYRIGHT_CLASSIFICATION}
                    WHERE COPYRIGHT_STRING = '{COPYRIGHT_STRING}';"""
            
            cursor.execute(sql)

        if COPYRIGHT_SOURCE:
            # Preparing query to create a database
            sql = f"""UPDATE COPYRIGHTS
                    SET COPYRIGHT_SOURCE = {COPYRIGHT_SOURCE}
                    WHERE COPYRIGHT_STRING = '{COPYRIGHT_STRING}';"""
            
            cursor.execute(sql)

        conn.close()

    def delete_entry(self, *, COPYRIGHT_STRING: str) -> bool:
        for i, j, k in [(COPYRIGHT_STRING, str, str)]:
            if type(i) != j and type(i) != k and type(i) != type(k):
                raise ValueError
        response = False
        try:
            # establishing the connection
            conn = psycopg2.connect(database=self.__database,
                                    user=self.__user,
                                    password=self.__password,
                                    host=self.__host,
                                    port=self.__port)

            # Creating a curser object using the cursor() method
            cursor = conn.cursor()
            conn.autocommit = True

            sql = f"""DELETE FROM COPYRIGHTS
                    WHERE COPYRIGHT_STRING = '{COPYRIGHT_STRING}'
                    RETURNING *;"""
            
            cursor.execute(sql)
            if len(cursor.fetchall()) > 0:
                response = True
        
        except (Exception, psycopg2.DatabaseError) as error:
            print(error)
        finally:
            conn.close()
            return response

    
    def get_entries(self, *, COPYRIGHT_SOURCE:str or None=None) -> list:
        for i, j, k in [(COPYRIGHT_SOURCE, int, None)]:
            if type(i) != j and type(i) != k and type(i) != type(k):
                raise ValueError
        try:
            # establishing the connection
            conn = psycopg2.connect(database=self.__database,
                                    user=self.__user,
                                    password=self.__password,
                                    host=self.__host,
                                    port=self.__port)

            # Creating a curser object using the cursor() method
            cursor = conn.cursor()
            conn.autocommit = True

            sql = f"""SELECT * FROM COPYRIGHTS"""

            if COPYRIGHT_SOURCE:
                sql += f" WHERE COPYRIGHT_SOURCE = {COPYRIGHT_SOURCE}"
            
            sql += ";"
            cursor.execute(sql)
            
            list_entries = cursor.fetchall()
        except (Exception, psycopg2.DatabaseError) as error:
            print(error)
            list_entries = []
        finally:
            conn.close()
            return list_entries


def main():
    print(DATABASE)
    class1 = ManageDatabase()
    print(class1.create_entry(COPYRIGHT_STRING="h0"))
    print(class1.create_entry(COPYRIGHT_STRING="hi", COPYRIGHT_CLASSIFICATION=1, COPYRIGHT_SOURCE=1))
    print(class1.create_entry(COPYRIGHT_STRING="hii", COPYRIGHT_CLASSIFICATION=1, COPYRIGHT_SOURCE=1))
    print(class1.create_entry(COPYRIGHT_STRING="hiii", COPYRIGHT_CLASSIFICATION=1, COPYRIGHT_SOURCE=2))
    # print(class1.delete_entry(COPYRIGHT_STRING="h0"))
    # print(class1.delete_entry(COPYRIGHT_STRING="hi"))
    # print(class1.delete_entry(COPYRIGHT_STRING="hii"))
    # print(class1.delete_entry(COPYRIGHT_STRING="hiii"))
    print(class1.get_entries())
    print(class1.get_entries(COPYRIGHT_SOURCE=1))

if __name__ == "__main__":
    main()