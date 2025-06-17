from __future__ import annotations
from flask import Flask, request, Response
from flask.typing import RouteCallable
from typing import Annotated
from injector import inject, provider, singleton, Module

import qbittorrent_add_trackers
from qbittorrent_add_trackers.component.add_trackers_services import AddTrackersServices
from qbittorrent_add_trackers.component.qbittorrent_manager import QbittorrentManager
from qbittorrent_add_trackers.controller.restapi_view import RestApiView

RestApiViewQualifier = Annotated[RestApiView, "RestApiView"]

class ControllerModule(Module):

  @singleton
  @provider
  def view(self, add_trackers_services: AddTrackersServices) -> RestApiViewQualifier:
    return RestApiView.as_view("add_trackers", add_trackers_services)
  
  @singleton
  @provider
  def flask_app(self, route: RestApiViewQualifier) -> Flask:
    app = Flask(qbittorrent_add_trackers.__name__)
    app.add_url_rule("/torrents/<hash_id>", view_func=route)
    return app