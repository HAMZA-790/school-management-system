import pyodbc
from app.utils.logger import logger

def setup_database():
    # Connect to master database first to create school_db
    server = r"localhost"
    master_connection_string = f"Driver={{ODBC Driver 17 for SQL Server}};Server={server};Database=master;Trusted_Connection=yes;"
    
    try:
        connection = pyodbc.connect(master_connection_string, autocommit=True)
        cursor = connection.cursor()
        
        # Create Database if it doesn't exist
        cursor.execute("""
            IF NOT EXISTS (SELECT * FROM sys.databases WHERE name = 'school_db')
            BEGIN
                CREATE DATABASE school_db;
            END
        """)
        logger.info("Database school_db checked/created successfully.")
        
        cursor.close()
        connection.close()

        # Reconnect to school_db
        school_db_connection_string = f"Driver={{ODBC Driver 17 for SQL Server}};Server={server};Database=school_db;Trusted_Connection=yes;"
        connection = pyodbc.connect(school_db_connection_string)
        cursor = connection.cursor()

        # Create Tables
        tables = {}
        tables['users'] = """
            IF NOT EXISTS (SELECT * FROM sysobjects WHERE name='users' and xtype='U')
            CREATE TABLE users (
              id INT IDENTITY(1,1) PRIMARY KEY,
              username VARCHAR(50) NOT NULL UNIQUE,
              password VARCHAR(255) NOT NULL
            )
        """

        tables['students'] = """
            IF NOT EXISTS (SELECT * FROM sysobjects WHERE name='students' and xtype='U')
            CREATE TABLE students (
              id INT IDENTITY(1,1) PRIMARY KEY,
              name VARCHAR(100) NOT NULL,
              class VARCHAR(50) NOT NULL,
              age INT NOT NULL
            )
        """

        tables['teachers'] = """
            IF NOT EXISTS (SELECT * FROM sysobjects WHERE name='teachers' and xtype='U')
            CREATE TABLE teachers (
              id INT IDENTITY(1,1) PRIMARY KEY,
              name VARCHAR(100) NOT NULL,
              subject VARCHAR(100) NOT NULL
            )
        """

        tables['attendance'] = """
            IF NOT EXISTS (SELECT * FROM sysobjects WHERE name='attendance' and xtype='U')
            CREATE TABLE attendance (
              id INT IDENTITY(1,1) PRIMARY KEY,
              student_id INT NOT NULL,
              date DATE NOT NULL,
              status VARCHAR(20) NOT NULL CHECK (status IN ('Present', 'Absent', 'Late')),
              FOREIGN KEY (student_id) REFERENCES students(id) ON DELETE CASCADE
            )
        """

        tables['fees'] = """
            IF NOT EXISTS (SELECT * FROM sysobjects WHERE name='fees' and xtype='U')
            CREATE TABLE fees (
              id INT IDENTITY(1,1) PRIMARY KEY,
              student_id INT NOT NULL,
              amount DECIMAL(10,2) NOT NULL,
              date DATE NOT NULL,
              FOREIGN KEY (student_id) REFERENCES students(id) ON DELETE CASCADE
            )
        """

        for table_name in tables:
            cursor.execute(tables[table_name])
            logger.info(f"Table {table_name} checked/created successfully.")

        # Insert Sample Data
        
        # Check if admin user exists
        cursor.execute("SELECT * FROM users WHERE username='admin'")
        if not cursor.fetchone():
            cursor.execute("INSERT INTO users (username, password) VALUES ('admin', 'adminpassword')")
        
        # Check if students exist
        cursor.execute("SELECT COUNT(*) FROM students")
        if cursor.fetchone()[0] == 0:
            cursor.execute("INSERT INTO students (name, class, age) VALUES ('John Doe', '10th', 15), ('Jane Smith', '9th', 14)")
            
        # Check if teachers exist
        cursor.execute("SELECT COUNT(*) FROM teachers")
        if cursor.fetchone()[0] == 0:
            cursor.execute("INSERT INTO teachers (name, subject) VALUES ('Mr. Anderson', 'Math'), ('Mrs. Davis', 'Science')")

        connection.commit()
        logger.info("Sample data checked/inserted successfully.")

    except pyodbc.Error as e:
        logger.error(f"Error while connecting to MSSQL: {e}")
    finally:
        if 'connection' in locals():
            try:
                connection.close()
                logger.info("MSSQL connection is closed")
            except pyodbc.Error:
                pass

if __name__ == "__main__":
    setup_database()
