import logging

from flask.views import MethodView

from qbittorrent_add_trackers.component.add_trackers_services import AddTrackersServices

logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)


class RestApiView(MethodView):
  init_every_request = False

  def __init__(self, add_trackers_services: AddTrackersServices) -> None:
    super().__init__()
    self.add_trackers_services = add_trackers_services

  def patch(self, hash_id: str):
    try:
      self.add_trackers_services.add_trackers(hash_id)
      return "Trackers added successfully", 200
    except Exception as e:
      logger.error(f"Failed to add trackers to torrent with hash {hash_id}: {e}", exc_info=True)
      
