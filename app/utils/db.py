import mysql.connector
from mysql.connector import Error
from app.utils.logger import logger

class Database:
    def __init__(self, host="localhost", user="root", password="your_password", database="school_db"):
        self.host = host
        self.user = user
        self.password = password
        self.database = database
        self.connection = None

    def get_connection(self):
        try:
            if self.connection and self.connection.is_connected():
                return self.connection
            
            self.connection = mysql.connector.connect(
                host=self.host,
                user=self.user,
                password=self.password,
                database=self.database
            )
            if self.connection.is_connected():
                logger.info("Successfully connected to the database")
                return self.connection
        except Error as e:
            logger.error(f"Error connecting to MySQL Database: {e}")
            return None

    def close_connection(self):
        if self.connection and self.connection.is_connected():
            self.connection.close()
            logger.info("MySQL connection is closed")

# Singleton instance
db = Database()

def get_db_connection():
    return db.get_connection()
