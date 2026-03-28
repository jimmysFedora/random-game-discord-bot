# 🎮 random-game-discord-bot

> Can't decide what to play with friends? Let the Doggo of Games decide.

A lightweight Discord bot that rolls a random video game from a csv list.

---

## Features

| Command | Description |
|--------|-------------|
| `/list` | Lists all games from `games.csv` (supports live editing — no restart needed!) |
| `/roll` | Picks a random game via `random.choice()` |
| `/add`  | Adds a game to the list (one at a time) |
| `/rm`   | Removes a game from the list (one at a time) |

The `games.csv` supports **live editing** — add or remove games while the bot is running and `/list` will reflect the changes immediately.

Built with Python. Available as a Docker image for easy self-hosting.

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

### Option A — Docker Compose (recommended)

1. **Install Docker** — [get-started](https://www.docker.com/get-started/)

2. **Create `docker-compose.yaml`:**

```yaml
services:
  discord-gamebot:
    image: ghcr.io/jimmysfedora/random-game-discord-bot:latest
    container_name: discord-gamebot
    restart: unless-stopped
    env_file:
      - .env
    volumes:
      - ./games.csv:/app/games.csv
```

3. **Create `.env`** in the same directory:

```env
TOKEN=YOUR_BOT_TOKEN_HERE
```

4. **Create `games.csv`** in the same directory and populate it with your games (one per line).

5. **Verify** file structure

```
.
├── docker-compose.yaml
├── .env
└── games.csv
```

5. **Start the bot:**

```bash
docker compose up -d
```

6. **Verify it's running:**

```bash
docker ps
docker logs discord-gamebot
```

7. **Invite the bot** to your server using the OAuth2 URL generated in the Developer Portal.

---

### Option B — Python (manual)

1. **Install Python** — [python.org](https://www.python.org/)

2. **Clone the repo:**

```bash
git clone https://github.com/jimmysFedora/random-game-discord-bot
cd random-game-discord-bot
```

3. **Create `.env`** in the project root:

```env
TOKEN=YOUR_BOT_TOKEN_HERE
```

4. Move **`games.csv`** and **`random_game.py`** into same directory as .env and edit csv with desired games.

5. **Run the bot:**

```bash
python random_game.py
```

6. **Invite the bot** to your server using the OAuth2 URL from the Developer Portal.
