from injector import inject, provider, singleton, Module
from config import ConfigurationSet
from qbittorrentapi import Client

from qbittorrent_add_trackers.component.add_trackers_services import AddTrackersServices
from qbittorrent_add_trackers.component.trackers_fetcher import TrackersFetcher
from qbittorrent_add_trackers.component.qbittorrent_manager import QbittorrentManager
from cachetools import TTLCache


class ComponentModule(Module):

  @singleton
  @provider
  def qbittorrent_client(self, config: ConfigurationSet) -> Client:
    return Client(config.qbittorrent.url, username=config.qbittorrent.username, password=config.qbittorrent.password)
  
  @singleton
  @provider
  def qbittorrent_manager(self, client: Client) -> QbittorrentManager:
    return QbittorrentManager(client)
  
  @singleton
  @provider
  def ttl_cache(self, config: ConfigurationSet) -> TTLCache:
    return TTLCache(maxsize=config.cache.maxsize, ttl=config.cache.ttl)
  
  @singleton
  @provider
  def trackers_fetcher(self, config: ConfigurationSet, ttl_cache: TTLCache) -> TrackersFetcher:
    return TrackersFetcher(ttl_cache, config.trackers.list_urls, config.trackers.individuals)
  
  @singleton
  @provider
  def add_trackers_services(self, trackers_fetcher: TrackersFetcher, qbittorrent_manager: QbittorrentManager) -> AddTrackersServices:
    return AddTrackersServices(trackers_fetcher, qbittorrent_manager)
  
  
  

