import pytest
from unittest.mock import patch, MagicMock
from app.services.auth_service import AuthService
from app.models.user_model import User

@patch('app.services.auth_service.get_db_connection')
def test_login_success(mock_get_db_connection):
    # Mocking database connection and cursor
    mock_conn = MagicMock()
    mock_cursor = MagicMock()
    mock_get_db_connection.return_value = mock_conn
    mock_conn.cursor.return_value = mock_cursor

    # Simulate database returning a user
    mock_cursor.fetchone.return_value = {'id': 1, 'username': 'admin'}

    user, message = AuthService.login('admin', 'adminpassword')

    assert isinstance(user, User)
    assert user.username == 'admin'
    assert message == "Login successful"
    mock_cursor.execute.assert_called_once()

@patch('app.services.auth_service.get_db_connection')
def test_login_failure(mock_get_db_connection):
    mock_conn = MagicMock()
    mock_cursor = MagicMock()
    mock_get_db_connection.return_value = mock_conn
    mock_conn.cursor.return_value = mock_cursor

    # Simulate database returning no user (invalid credentials)
    mock_cursor.fetchone.return_value = None

    user, message = AuthService.login('wrong', 'wrongpass')

    assert user is None
    assert message == "Invalid username or password."

@patch('app.services.auth_service.get_db_connection')
def test_login_db_error(mock_get_db_connection):
    mock_get_db_connection.return_value = None

    user, message = AuthService.login('admin', 'adminpassword')

    assert user is None
    assert message == "Database connection failed."
