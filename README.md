# random-game-discord-bot
Can't decide what to play with friends? This fixes it, as your custom discord bot will roll a random video game from a csv file.

**Features:**
- A Python app built to establish websocket connection with Discord for real-time processing of commands.
- `/list` - lists all the games from the provided `games.csv` file (csv file supports live editing!)
- `/roll` - rolls a random game using `random.choice()`
- Available as a Docker container.


**Screenshots:**

<img width="349" height="910" alt="Screenshot 2026-02-22 at 11 52 45" src="https://github.com/user-attachments/assets/75319c45-712c-4df8-94e2-e1a3bc03c3a1" />

**Requirements:**
- A key generated from an app on Discord Developer Portal
- Bot must have `applications.commands` and `bot` scope with required scopes and permissions

**Install instructions:**
- Clone repo
- Create environment file with TOKEN entry with key from Discord Developer Portal
- Edit provided `games.csv` with desired games
- Run `docker compose up -d`
- Invite bot to server from OAuth2 link

**Docker Compose:**
```bash
services:
  discord-bot:
    build: .
    container_name: doggo-game-bot
    restart: unless-stopped
    env_file:
      - .env
    volumes:
      - ./data/games.csv:/app/games.csv
```

**Example ENV:**
```
TOKEN=YOURKEYHERE
```
