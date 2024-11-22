import pytest
from unittest.mock import MagicMock

from qbittorrent_add_trackers.component.add_trackers_services import AddTrackersServices


@pytest.fixture
def mock_trackers_fetcher():
  mock_fetcher = MagicMock()
  mock_fetcher.get_all.return_value = {"tracker1", "tracker2"}
  return mock_fetcher

@pytest.fixture
def mock_qbittorrent_manager():
  mock_manager = MagicMock()
  mock_manager.add_trackers.return_value = None
  mock_manager.get_trackers.return_value = {"tracker2", "tracker3"}
  return mock_manager


def test_normal_flow(mock_trackers_fetcher, mock_qbittorrent_manager):
  add_trackers_services = AddTrackersServices(mock_trackers_fetcher, mock_qbittorrent_manager)
  add_trackers_services.add_trackers("hash")
  mock_qbittorrent_manager.add_trackers.assert_called_once_with("hash", {"tracker1", "tracker2", "tracker3"})
  
  