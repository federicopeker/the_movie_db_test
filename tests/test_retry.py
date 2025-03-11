from unittest.mock import patch

import requests

from app.utils.retry import make_request_with_retry


def test_request_fails_logs_error_and_returns_none(capsys):
    with patch("app.utils.retry.requests_retry_session") as mock_session:
        mock_session.return_value.request.side_effect = requests.exceptions.RequestException(
            "Error"
        )
        response = make_request_with_retry("http://example.com")
        assert response is None
        captured = capsys.readouterr()
        assert "Request failed: Error" in captured.err


def test_request_succeeds_returns_response():
    with patch("app.utils.retry.requests_retry_session") as mock_session:
        mock_response = mock_session.return_value.request.return_value
        mock_response.raise_for_status.return_value = None
        mock_response.json.return_value = {"key": "value"}
        response = make_request_with_retry("http://example.com")
        assert response.json() == {"key": "value"}
