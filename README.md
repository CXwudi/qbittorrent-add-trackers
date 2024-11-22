# qBittorrent Add Trackers

A small flask app that automatically adds trackers to qBittorrent when new torrents are added.

It simply just exposed a `PATCH /torrents/{hash}` endpoint that triggers the tracker addition process, and qBittorrent can be configured to run the script when a torrent is added.

## Features

- Automatically fetches updated trackers from configurable sources
- Integrates with qBittorrent via Web API
- Caches tracker lists to minimize external requests
- Docker support for easy deployment
- Configurable settings via YAML configuration
- Supports both tracker list URLs and individual tracker URLs

## Prerequisites

- Python 3.12+
- qBittorrent with Web UI enabled
- Docker (optional, for containerized deployment)

## Installation

### Docker Compose Setup

```sh
# .env
QBITTORRENT_WEBUI_PORT=8080
QBITTORRENT_TORRENTING_PORT=39001
APP__FLASK__PORT=8080
```

```yaml
# compose.yml
services:

  qbittorrent-add-trackers:
    image: cxwudi/qbittorrent-add-trackers:latest
    container_name: qbittorrent-add-trackers
    environment:
      - APP__QBITTORRENT__URL=http://qbittorrent:${QBITTORRENT_WEBUI_PORT}
      - APP__QBITTORRENT__PASSWORD=123456
      - APP__FLASK__PORT=${APP__FLASK__PORT:-8080}
    volumes:
      - ./config.yaml:/app/config.yaml

  qbittorrent:
    # please set user/pass to admin/123456
    image: linuxserver/qbittorrent
    container_name: qbittorrent
    environment:
      - PUID=1000
      - PGID=1000
      - TZ=America/New_York
      - WEBUI_PORT=${QBITTORRENT_WEBUI_PORT}
      - TORRENTING_PORT=${QBITTORRENT_TORRENTING_PORT}
      - APP_PORT=${APP__FLASK__PORT:-8080}
    volumes:
      - ./data:/config
      - ./downloads:/downloads
      - ./run_on_add.sh:/run_on_add.sh
    ports:
      - ${QBITTORRENT_WEBUI_PORT}:${QBITTORRENT_WEBUI_PORT}
      - ${QBITTORRENT_TORRENTING_PORT}:${QBITTORRENT_TORRENTING_PORT}/tcp
      - ${QBITTORRENT_TORRENTING_PORT}:${QBITTORRENT_TORRENTING_PORT}/udp
    restart: unless-stopped

```

Where `run_on_add.sh` is:

```sh
#!/bin/bash

TORRENT_HASH=$1 # hash of torrent

curl -v -X PATCH http://qbittorrent-add-trackers:${APP_PORT:-8080}/torrents/$TORRENT_HASH
```

And `config.yaml` is your own settings based on `config.base.yaml`:

```yaml
qbittorrent: # replace with your actual qBittorrent instance, or let some of these values be empty and set the corresponding environment variables
  host: "localhost"
  port: 8080
  username: "admin"
  password: "adminadmin"

flask:
  host: "0.0.0.0"
  port: 5000

trackers:
  # URLs that contain lists of trackers
  tracker_list_urls:
    - "https://example.com/trackers.txt"
  # Individual tracker URLs
  individual_trackers:
    - "udp://tracker.example.com:6969/announce"
```

All configuration options can be overridden via environment variables, with a prefix of `APP__`.
For example, to override the `qbittorrent.host` and `qbittorrent.port` of the qBittorrent instance, you can set `APP__QBITTORRENT__HOST` and `APP__QBITTORRENT__PORT` respectively.

### Configuring qBittorrent

Once the qBittorrent instance is running, you need to configure it to run the script when a torrent is added.

1. Open qBittorrent Preferences
2. Go to "Downloads" section
3. Under "Run external program on torrent added", add the following command:
   ```bash
   /run_on_add.sh "%K"
   ```
   - Replace `/run_on_add.sh` with the actual path to the script
   - `%K` is the torrent hash placeholder that qBittorrent will replace automatically

The script will make a PATCH request to the service with the torrent hash, triggering the tracker addition process.

### For non Docker users

You can run `poetry run package` to build a standalone executable.

And then place the `config.yaml` file in the same directory as the executable, and run it.

## Development

This project uses dev containers, so as long as you have Docker and VSCode installed, you can just open the project in VSCode and it will automatically set up the dev container for you.

### Installing Dependencies

```bash
poetry install
```

### Running Tests

```bash
poetry run pytest
```

### Project Structure

- `component/`: Core business logic components
  - `qbittorrent_manager.py`: qBittorrent API integration
  - `trackers_fetcher.py`: Tracker list fetching and caching
- `config/`: Configuration management
- `controller/`: REST API endpoints
- `build_scripts/`: Docker and build utilities

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.