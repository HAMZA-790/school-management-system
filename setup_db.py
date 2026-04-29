import mysql.connector
from mysql.connector import Error
from app.utils.logger import logger

def setup_database():
    try:
        # Connect to MySQL server (without specifying DB first)
        connection = mysql.connector.connect(
            host="localhost",
            user="root",
            password="your_password"
        )
        if connection.is_connected():
            cursor = connection.cursor()
            
            # Create Database
            cursor.execute("CREATE DATABASE IF NOT EXISTS school_db")
            logger.info("Database school_db created successfully.")
            
            # Switch to school_db
            cursor.execute("USE school_db")

            # Create Tables
            tables = {}
            tables['users'] = (
                "CREATE TABLE IF NOT EXISTS users ("
                "  id INT AUTO_INCREMENT PRIMARY KEY,"
                "  username VARCHAR(50) NOT NULL UNIQUE,"
                "  password VARCHAR(255) NOT NULL"
                ") ENGINE=InnoDB"
            )

            tables['students'] = (
                "CREATE TABLE IF NOT EXISTS students ("
                "  id INT AUTO_INCREMENT PRIMARY KEY,"
                "  name VARCHAR(100) NOT NULL,"
                "  class VARCHAR(50) NOT NULL,"
                "  age INT NOT NULL"
                ") ENGINE=InnoDB"
            )

            tables['teachers'] = (
                "CREATE TABLE IF NOT EXISTS teachers ("
                "  id INT AUTO_INCREMENT PRIMARY KEY,"
                "  name VARCHAR(100) NOT NULL,"
                "  subject VARCHAR(100) NOT NULL"
                ") ENGINE=InnoDB"
            )

            tables['attendance'] = (
                "CREATE TABLE IF NOT EXISTS attendance ("
                "  id INT AUTO_INCREMENT PRIMARY KEY,"
                "  student_id INT NOT NULL,"
                "  date DATE NOT NULL,"
                "  status ENUM('Present', 'Absent', 'Late') NOT NULL,"
                "  FOREIGN KEY (student_id) REFERENCES students(id) ON DELETE CASCADE"
                ") ENGINE=InnoDB"
            )

            tables['fees'] = (
                "CREATE TABLE IF NOT EXISTS fees ("
                "  id INT AUTO_INCREMENT PRIMARY KEY,"
                "  student_id INT NOT NULL,"
                "  amount DECIMAL(10,2) NOT NULL,"
                "  date DATE NOT NULL,"
                "  FOREIGN KEY (student_id) REFERENCES students(id) ON DELETE CASCADE"
                ") ENGINE=InnoDB"
            )

            for table_name in tables:
                cursor.execute(tables[table_name])
                logger.info(f"Table {table_name} created successfully.")

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
            logger.info("Sample data inserted successfully.")

    except Error as e:
        logger.error(f"Error while connecting to MySQL: {e}")
    finally:
        if 'connection' in locals() and connection.is_connected():
            cursor.close()
            connection.close()
            logger.info("MySQL connection is closed")

if __name__ == "__main__":
    setup_database()
