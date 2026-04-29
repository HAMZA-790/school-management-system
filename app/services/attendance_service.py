from app.utils.db import get_db_connection
from app.utils.logger import logger

class AttendanceService:
    @staticmethod
    def mark_attendance(student_id, date, status):
        try:
            conn = get_db_connection()
            if not conn: return False, "DB Connection Error"
            cursor = conn.cursor()
            
            # Check if attendance already marked for the day
            cursor.execute("SELECT id FROM attendance WHERE student_id=? AND date=?", (student_id, date))
            if cursor.fetchone():
                return False, "Attendance already marked for this date"

            query = "INSERT INTO attendance (student_id, date, status) VALUES (?, ?, ?)"
            cursor.execute(query, (student_id, date, status))
            conn.commit()
            return True, "Attendance marked successfully"
        except Exception as e:
            logger.error(f"Error marking attendance: {e}")
            return False, str(e)
        finally:
            if 'cursor' in locals() and cursor: cursor.close()

    @staticmethod
    def get_attendance():
        try:
            conn = get_db_connection()
            if not conn: return []
            cursor = conn.cursor()
            query = """
            SELECT a.id, s.name as student_name, a.date, a.status 
            FROM attendance a 
            JOIN students s ON a.student_id = s.id
            ORDER BY a.date DESC
            """
            cursor.execute(query)
            columns = [column[0] for column in cursor.description]
            return [dict(zip(columns, row)) for row in cursor.fetchall()]
        except Exception as e:
            logger.error(f"Error fetching attendance: {e}")
            return []
        finally:
            if 'cursor' in locals() and cursor: cursor.close()
