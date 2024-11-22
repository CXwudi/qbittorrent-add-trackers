# qBittorrent Add Trackers

A small flask app that automatically adds trackers from tracker lists to a torrent when it is added into qBittorrent.

This app relies on the auto run script feature of qBittorrent to call a script when a torrent is added.

This app simply exposes a `PATCH /torrents/{hash}` endpoint which simply fetches a list of trackers and added them to the torrent of the given hash, done by the qBittorrent Web API. qBittorrent can be configured to curl the endpoint when a torrent is added.

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
# assuming your qbittorrent password is 123456
services:
  qbittorrent:
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

  qbittorrent-add-trackers:
    image: cxwudi/qbittorrent-add-trackers:latest
    container_name: qbittorrent-add-trackers
    environment:
      - APP__QBITTORRENT__URL=http://qbittorrent:${QBITTORRENT_WEBUI_PORT}
      - APP__QBITTORRENT__PASSWORD=123456
      - APP__FLASK__PORT=${APP__FLASK__PORT:-8080}
    volumes:
      - ./config.yaml:/app/config.yaml
    depends_on:
      - qbittorrent-app
    restart: unless-stopped # this is necessary as the container may start before qbittorrent is ready

```

Create a bash script `run_on_add.sh`:

```sh
#!/bin/bash

TORRENT_HASH=$1 # hash of torrent

curl -v -X PATCH http://qbittorrent-add-trackers:${APP_PORT:-8080}/torrents/$TORRENT_HASH
```

Create a config file `config.yaml` based on [`config.base.yaml`](config.base.yaml):

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
  tracker_list_urls: [
    'https://cf.trackerslist.com/best.txt',
    'https://newtrackon.com/api/stable',
    'https://raw.githubusercontent.com/ngosang/trackerslist/master/trackers_all.txt'
  ]
  # Individual tracker URLs
  individual_trackers: [
    'http://open.acgtracker.com:1096/announce'
  ]
```

The app will read the included [`config.base.yaml`](config.base.yaml) from the current working directory first, and then override it with your provided `config.yaml` file in the same directory.

Optionally, you can override the configuration via environment variables, with a prefix of `APP__`.
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

Here is the screenshot of the qBittorrent settings:

![image](https://s2.loli.net/2024/11/23/nPR6yiUXoJ8QCLb.png)

### For non Docker users

You can run `poetry run package` to build a standalone executable.

And then place your `config.yaml` file and [`config.base.yaml`](config.base.yaml) in the same directory as the executable, and run it.

## Development

This project uses dev containers, so as long as you have Docker and VSCode installed, you can just open the project in VSCode and it will automatically set up the dev container for you.

Otherwise, use Python 3.12 and install poetry and poethepoet:

```bash
pip install poetry poethepoet
```

### Installing Dependencies

```bash
poetry install
```

### Running Tests

```bash
poetry run pytest
```

### Project Structure

- `qbittorrent_add_trackers/`: The main project
  - `component/`: Core business logic components
    - `qbittorrent_manager.py`: qBittorrent API integration
    - `trackers_fetcher.py`: Tracker list fetching and caching
  - `config/`: Configuration management
  - `controller/`: REST API endpoints
- `build_scripts/`: Docker and build utilities

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.
