import pytest, logging
from unittest.mock import MagicMock, patch
from qbittorrent_add_trackers.component.trackers_fetcher import TrackersFetcher

logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

@pytest.fixture
def mock_cache():
    cache = MagicMock()
    cache.__contains__.side_effect = lambda key: key in cache._store # Simulate the 'in' operator
    cache._store = {}
    cache.__getitem__.side_effect = cache._store.__getitem__
    cache.__setitem__.side_effect = cache._store.__setitem__
    return cache


def test_get_one(mock_cache):
  fetcher = TrackersFetcher(mock_cache, ["https://cf.trackerslist.com/all.txt"])
  all = fetcher._get("https://cf.trackerslist.com/all.txt")
  logger.info(all)
  assert len(all) > 100


def test_cache(mock_cache):
  # Assuming this URL returns ["tracker1", "tracker2"]
  url = "https://example.com/trackers.txt"
  sample_response = ["tracker1", "tracker2"]

  # Mocking the requests.get call to return a sample response
  with patch('requests.get') as mock_get:
    mock_get.return_value.status_code = 200
    mock_get.return_value.text = "\n".join(sample_response)

    fetcher = TrackersFetcher(mock_cache, [url])

    # First call - expects to fetch the data and populate the cache
    result = fetcher._get_one(url)
    assert result == sample_response
    assert url in mock_cache  # Checks if the URL is in cache
    assert mock_cache[url] == sample_response  # Verifies the cache content

    # Set up the cache mock return value for the second call
    mock_cache.__contains__.return_value = True
    mock_cache.__getitem__.return_value = sample_response
    
    # Second call - expects to use the cache
    result = fetcher._get_one(url)
    assert result == sample_response  # Expect same response
    mock_get.assert_called_once_with(url)  # Ensure requests.get was only called once  


  
  