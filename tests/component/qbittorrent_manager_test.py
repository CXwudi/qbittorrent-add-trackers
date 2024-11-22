import pytest
from unittest.mock import MagicMock
from qbittorrent_add_trackers.component.qbittorrent_manager import QbittorrentManager


@pytest.fixture
def mock_client():
    return MagicMock()


def test_login_success(mock_client):
    qbittorrent_client = QbittorrentManager(mock_client)
    qbittorrent_client.qbittorrent.auth_log_in.return_value = True

    qbittorrent_client.login()

    mock_client.auth_log_in.assert_called_once()


def test_login_failure(mock_client):
    qbittorrent_client = QbittorrentManager(mock_client)
    qbittorrent_client.qbittorrent.auth_log_in.side_effect = Exception("Login failed")

    with pytest.raises(Exception):
        qbittorrent_client.login()

    mock_client.auth_log_in.assert_called_once()
