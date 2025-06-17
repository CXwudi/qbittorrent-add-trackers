from qbittorrentapi import Client
import logging

logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)


class QbittorrentManager:

  def __init__(self, client: Client):
    """
    A wrapper for interacting with the qBittorrent client.
    """
    self.qbittorrent = client

  def login(self):
    """
    Logs in to the qBittorrent client.

    Raises:
        Exception: If an error occurs during the login process.

    """
    try:
      self.qbittorrent.auth_log_in()
      logger.info("Logged in to qbittorrent")
    except Exception as e:
      logger.error(e)
      raise e

  def logout(self):
    """
    Logs out of the qBittorrent client.
    """
    self.qbittorrent.auth_log_out()
    logger.info("Logged out of qbittorrent")


  def get_trackers(self, hash: str) -> set[str]:
    """
    Retrieves the trackers of the torrent with the given hash.

    Args:
        hash (str): The hash of the torrent to retrieve trackers for.

    Returns:
        set[str]: The trackers of the torrent with the given hash.

    Raises:
        Exception: If an error occurs during the tracker retrieval process.

    """
    try:
      trackers = self.qbittorrent.torrents_trackers(hash)
      logger.info(f"Retrieved trackers for torrent with hash {hash}")
      return { t['url'] for t in trackers }
    except Exception as e:
      logger.error(f"Failed to retrieve trackers for torrent with hash {hash}: {e}", exc_info=True)
      raise e

  def add_trackers(self, hash: str, urls: set[str]):
    """
    Adds trackers to the torrent with the given hash.

    Args:
        hash (str): The hash of the torrent to add trackers to.
        urls (set[str]): The URLs of the trackers to add.

    Raises:
        Exception: If an error occurs during the tracker addition process.

    """
    try:
      self.qbittorrent.torrents_add_trackers(hash, urls = urls)
      logger.info(f"Added {len(urls)} trackers to torrent with hash {hash}")
    except Exception as e:
      logger.error(f"Failed to add trackers to torrent with hash {hash}: {e}", exc_info=True)
      raise e
