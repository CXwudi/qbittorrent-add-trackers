import logging

from qbittorrent_add_trackers.component.qbittorrent_manager import QbittorrentManager
from qbittorrent_add_trackers.component.trackers_fetcher import TrackersFetcher

logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

class AddTrackersServices:

  def __init__(self, trackers_fetcher: TrackersFetcher, qbittorrent_manager: QbittorrentManager):

    self.trackers_fetcher = trackers_fetcher
    self.qbittorrent_manager = qbittorrent_manager

  def add_trackers(self, hash: str):
    """
    Adds trackers to the torrent with the given hash.

    Args:
        hash (str): The hash of the torrent to add trackers to.
    """
    trackers_web = self.trackers_fetcher.get_all()
    trackers_torrent = self.qbittorrent_manager.get_trackers(hash)

    merged_trackers = trackers_web | trackers_torrent
    self.qbittorrent_manager.add_trackers(hash, merged_trackers)
    pass