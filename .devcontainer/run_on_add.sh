#!/bin/bash

TORRENT_HASH=$1 # hash of torrent

curl -v -X PATCH http://devcontainer:${APP_PORT:-8080}/torrents/$TORRENT_HASH
