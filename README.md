# random-game-discord-bot

A lightweight Discord bot that picks a random game from a list stored in SQLite.

---

## Features

| Command | Description |
|--------|-------------|
| `/list` | Lists all games, sorted alphabetically (split across messages if long) |
| `/roll` | Picks a random game |
| `/add`  | Adds a game, up to 100 characters (duplicates are ignored, case-insensitive) |
| `/rm`   | Removes a game, with autocomplete (case-insensitive) |

Games are stored in `data/games.db` (override with the `DB_PATH` env var). On first start, if the database is empty and a `games.csv` (one game per line) sits next to it, the games are imported from it.

Built with Python. Runs as a rootless Podman container or directly with uv.

---

## Screenshots

<img width="349" height="910" alt="Bot in action" src="https://github.com/user-attachments/assets/75319c45-712c-4df8-94e2-e1a3bc03c3a1" />

---

## Requirements

### 1. Create a Discord App

- Head to the [Discord Developer Portal](https://discord.com/developers/applications) and create a new application
- Under **Bot**, generate and copy your token

<img width="1391" height="582" alt="Discord Developer Portal" src="https://github.com/user-attachments/assets/7dd7e7e4-e40a-42c1-a080-134fe2ff425f" />

### 2. Set Bot Permissions

Under **OAuth2 → URL Generator**, enable the following:

- **Scopes:** `bot`, `applications.commands`
- **Bot Permissions:** `Send Messages`, `Read Messages/View Channels`

<img width="1460" height="570" alt="OAuth2 Scopes" src="https://github.com/user-attachments/assets/a313e3fe-2919-4723-aae6-538bb3a30369" />
<img width="1072" height="762" alt="Bot Permissions" src="https://github.com/user-attachments/assets/72d4abbb-89b1-4a21-b166-b1498fa831dd" />

---

## Setup

### Option A — Podman (recommended)

Runs the bot as a rootless container managed by systemd, using a [Quadlet](https://docs.podman.io/en/latest/markdown/podman-systemd.unit.5.html) unit. Requires Podman 5+.

1. **Clone the repo** into your home directory and build the image:

```bash
git clone https://github.com/jimmysFedora/random-game-discord-bot ~/random-game-discord-bot
cd ~/random-game-discord-bot
podman build -t random-game-bot .
```

2. **Create `.env`** in the repo root:

```env
TOKEN=YOUR_BOT_TOKEN_HERE
```

3. **Create the `data` folder** for the database:

```bash
mkdir data
```

   *(Optional)* Seed the game list (one game per line) before the first start. Otherwise use `/add`.

```bash
cp games.example.csv data/games.csv
```

4. **Install and start the service:**

```bash
mkdir -p ~/.config/containers/systemd
cp random-game-bot.container ~/.config/containers/systemd/
systemctl --user daemon-reload
systemctl --user start random-game-bot
```

   If you cloned somewhere other than `~/random-game-discord-bot`, edit the paths in the copied `random-game-bot.container` first.

5. **Keep it running after you log out** (and start it at boot):

```bash
loginctl enable-linger $USER
```

6. **Check it's running:**

```bash
systemctl --user status random-game-bot
journalctl --user -u random-game-bot -f
```

7. **Invite the bot** to your server using the OAuth2 URL generated in the Developer Portal.

To update after pulling new code: `podman build -t random-game-bot . && systemctl --user restart random-game-bot`.

To run it once without systemd:

```bash
podman run -d --name random-game-bot --env-file .env \
  --userns keep-id:uid=1000,gid=1000 -v ./data:/app/data:Z localhost/random-game-bot
```

---

### Option B — uv (manual)

1. **Install uv** — [docs.astral.sh/uv](https://docs.astral.sh/uv/getting-started/installation/). uv installs the right Python version (3.12) itself.

2. **Clone the repo:**

```bash
git clone https://github.com/jimmysFedora/random-game-discord-bot
cd random-game-discord-bot
```

3. **Create `.env`** in the project root:

```env
TOKEN=YOUR_BOT_TOKEN_HERE
```

4. *(Optional)* **Seed the game list** from the example (or write your own, one game per line):

```bash
mkdir -p data && cp games.example.csv data/games.csv
```

5. **Run the bot** from the project root. uv creates the virtual environment and installs dependencies on first run. The database is created at `data/games.db`, seeded from `data/games.csv` if present.

```bash
uv run random-game-bot
```

6. **Invite the bot** to your server using the OAuth2 URL from the Developer Portal.

---

## Development

```bash
uv run pytest           # run tests
uv run ruff check .     # lint
uv run ruff format .    # format
```

To run the tests and lint in a clean container instead (nothing is written to the repo):

```bash
podman run --rm --mount type=image,src=ghcr.io/astral-sh/uv:0.12,dst=/uvimg \
  -v .:/src:ro,Z -w /src -e UV_PROJECT_ENVIRONMENT=/tmp/venv -e UV_CACHE_DIR=/tmp/uv-cache \
  docker.io/library/python:3.12-slim \
  sh -c '/uvimg/uv run -q --locked pytest -p no:cacheprovider && /uvimg/uv run -q --locked ruff check --no-cache .'
```

```
src/random_game_bot/
  bot.py                    # database, commands, entry point
  __main__.py               # allows `python -m random_game_bot`
tests/                      # pytest tests using fake Discord interactions
games.example.csv           # example seed list
random-game-bot.container   # Podman Quadlet unit
data/                       # runtime data (database, optional seed CSV), git-ignored
```
