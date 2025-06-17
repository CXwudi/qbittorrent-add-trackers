import logging
from injector import Injector
from qbittorrent_add_trackers.config.di_module import ConfigModule
from qbittorrent_add_trackers.component.di_module import ComponentModule
from qbittorrent_add_trackers.controller.di_module import ControllerModule
from qbittorrent_add_trackers.flask_runner import FlaskRunner, FlaskRunnerModule

logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

injector = Injector([ConfigModule(), ComponentModule(), ControllerModule(), FlaskRunnerModule()])
flask_runner = injector.get(FlaskRunner)
flask_runner.setup()

flask_app = flask_runner.app

def main():
  """
  Entry point from uv.
  """
  flask_runner.run_flask()

if __name__ == "__main__":
  main()
