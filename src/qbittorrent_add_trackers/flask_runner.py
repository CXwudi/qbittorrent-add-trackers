import atexit
import logging

from config import ConfigurationSet
from flask import Flask
from injector import inject, provider, singleton, Module

from qbittorrent_add_trackers.component.qbittorrent_manager import QbittorrentManager

logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)


class FlaskRunner:
  def __init__(self, app: Flask, host: str, port: int, qbittorrent_manager: QbittorrentManager):
    self.app = app
    self.host = host
    self.port = port
    self.qbittorrent_manager = qbittorrent_manager

  def setup(self):
    logger.info(f"Logging in to qbittorrent")
    self.qbittorrent_manager.login()
    atexit.register(self._shutdown)

  def run_flask(self):
    from waitress import serve
    logger.info(f"Running Flask with waitress on {self.host}:{self.port}")
    serve(self.app, host=self.host, port=self.port)

  def _shutdown(self):
    logger.info("Logging out of qbittorrent")
    self.qbittorrent_manager.logout()


class FlaskRunnerModule(Module):

  @singleton
  @provider
  def flask_runner(self,
                   app: Flask,
                   config: ConfigurationSet,
                   qbittorrent_manager: QbittorrentManager) -> FlaskRunner:
    return FlaskRunner(app, config.flask.host, config.flask.port, qbittorrent_manager)
