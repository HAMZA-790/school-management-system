import pyodbc
from app.utils.logger import logger

class Database:
    def __init__(self, server=r"localhost", database="school_db"):
        self.server = server
        self.database = database
        # Using Windows Authentication by default
        self.connection_string = f"Driver={{ODBC Driver 17 for SQL Server}};Server={self.server};Database={self.database};Trusted_Connection=yes;"
        self.connection = None

    def get_connection(self):
        try:
            # Check if connection exists and is not closed
            if self.connection:
                try:
                    # Execute a dummy query to test the connection
                    self.connection.cursor().execute("SELECT 1")
                    return self.connection
                except pyodbc.Error:
                    self.connection = None
            
            self.connection = pyodbc.connect(self.connection_string)
            logger.info("Successfully connected to the database")
            return self.connection
        except pyodbc.Error as e:
            logger.error(f"Error connecting to MSSQL Database: {e}")
            return None

    def close_connection(self):
        if self.connection:
            try:
                self.connection.close()
                logger.info("MSSQL connection is closed")
            except pyodbc.Error:
                pass

# Singleton instance
db = Database()

def get_db_connection():
    return db.get_connection()
