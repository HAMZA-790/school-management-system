import pytest
from unittest.mock import patch, MagicMock
from app.services.student_service import StudentService

@patch('app.services.student_service.get_db_connection')
def test_add_student_success(mock_get_db_connection):
    mock_conn = MagicMock()
    mock_cursor = MagicMock()
    mock_get_db_connection.return_value = mock_conn
    mock_conn.cursor.return_value = mock_cursor

    success, message = StudentService.add_student('Test Student', '10th', 15)

    assert success is True
    assert message == "Student added successfully"
    mock_cursor.execute.assert_called_once()
    mock_conn.commit.assert_called_once()

@patch('app.services.student_service.get_db_connection')
def test_get_all_students(mock_get_db_connection):
    mock_conn = MagicMock()
    mock_cursor = MagicMock()
    mock_get_db_connection.return_value = mock_conn
    mock_conn.cursor.return_value = mock_cursor

    # Simulate database returning students
    mock_cursor.fetchall.return_value = [
        {'id': 1, 'name': 'John', 'class': '10th', 'age': 15},
        {'id': 2, 'name': 'Jane', 'class': '9th', 'age': 14}
    ]

    students = StudentService.get_all_students()

    assert len(students) == 2
    assert students[0].name == 'John'
    assert students[1].name == 'Jane'

@patch('app.services.student_service.get_db_connection')
def test_delete_student(mock_get_db_connection):
    mock_conn = MagicMock()
    mock_cursor = MagicMock()
    mock_get_db_connection.return_value = mock_conn
    mock_conn.cursor.return_value = mock_cursor

    success, message = StudentService.delete_student(1)

    assert success is True
    assert message == "Student deleted successfully"
    mock_cursor.execute.assert_called_once()
    mock_conn.commit.assert_called_once()
