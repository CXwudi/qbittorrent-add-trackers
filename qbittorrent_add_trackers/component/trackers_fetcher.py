import logging
from cachetools import TTLCache
import requests

logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)


class TrackersFetcher:

  def __init__(self, cache: TTLCache, tracker_list_urls: list[str], individual_trackers: list[str]) -> None:
    """
    Initializes a new instance of the TrackersFetcher class.

    Args:
        cache (TTLCache): The cache to use for storing trackers.
        tracker_list_urls (list[str]): A list of URLs that contains tracker URL lists.
        individual_trackers (list[str]): A list of tracker URLs, added individually by user.

    Returns:
        None
    """

    self.cache = cache
    self.trackers = tracker_list_urls
    self.individual_trackers = individual_trackers

  def get_all(self) -> set[str]:
    """
    Retrieves all trackers by calling the `_get_one` method for each URL in the `trackers` list.

    Returns:
        list[str]: A list of all the trackers retrieved from the URLs.
    """
    url_set = set(self.individual_trackers)
    for url in self.trackers:
      urls = self._get_one(url)
      url_set.update(urls)
    return url_set

  def _get_one(self, url: str) -> list[str]:
    """
    Retrieves a list of trackers from the specified URL.

    Args:
        url (str): The URL to fetch trackers from.

    Returns:
        list[str]: A list of trackers retrieved from the URL.

    This function checks if the URL is already in the cache. If it is, it logs a message and returns the cached trackers.
    If it is not in the cache, it logs a message, fetches the trackers from the URL, adds them to the cache, and returns the trackers.

    Raises:
        None
    """
    if url in self.cache:
      logger.info(f"Found {url} in cache")
      return self.cache[url]
    else:
      logger.info(f"Fetching {url} and adding to cache")
      try:
        urls = self._get(url)
      except Exception as e:
        logger.error(f"Failed to fetch {url}: {e}")
        return []
      self.cache[url] = urls
      return urls

  def _get(self, url: str) -> list[str]:
    """
    Retrieves a list of trackers from the specified URL.

    Args:
        url (str): The URL to fetch trackers from.

    Returns:
        list[str]: A list of trackers retrieved from the URL.

    Raises:
        Exception: If an error occurs during the retrieval process.
    """
    try:
      response = requests.get(url)
      if response.status_code != 200:
        raise Exception(f"Failed to fetch {url}")
      return [tracker for tracker in response.text.split("\n") if tracker.strip() != ""]
    except Exception as e:
      logger.error(e)
      raise e
