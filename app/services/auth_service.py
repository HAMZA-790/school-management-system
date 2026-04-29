from app.utils.db import get_db_connection
from app.models.user_model import User
from app.utils.logger import logger

class AuthService:
    @staticmethod
    def login(username, password):
        try:
            conn = get_db_connection()
            if not conn:
                return None, "Database connection failed."

            cursor = conn.cursor(dictionary=True)
            query = "SELECT * FROM users WHERE username = %s AND password = %s"
            cursor.execute(query, (username, password))
            result = cursor.fetchone()

            if result:
                user = User(result['id'], result['username'])
                return user, "Login successful"
            else:
                return None, "Invalid username or password."
        except Exception as e:
            logger.error(f"Error during login: {e}")
            return None, f"An error occurred: {str(e)}"
        finally:
            if 'cursor' in locals() and cursor:
                cursor.close()
