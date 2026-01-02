import app
from unittest.mock import patch

def test_students_endpoint():
    with patch("app.get_db_connection") as mock_db:
        mock_conn = mock_db.return_value
        mock_cursor = mock_conn.cursor.return_value
        mock_cursor.fetchall.return_value = []

        client = app.app.test_client()
        response = client.get("/students")

        assert response.status_code == 200
