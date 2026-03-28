# random-game-discord-bot
Can't decide what to play with friends? This fixes it, as your custom discord bot will roll a random video game from a csv file.

## Features
- A Python app built to establish websocket connection with Discord for real-time processing of commands.
- `/list` - lists all the games from the provided `games.csv` file (csv file supports live editing!)
- `/roll` - rolls a random game using `random.choice()`
- `/add` - adds a game to the list (must enter one at a time)`
- `/rm` - removes a game entry (must remove one game at a time)`
- Available as a Docker container for self-hosting needs.


## Screenshots

<img width="349" height="910" alt="Screenshot 2026-02-22 at 11 52 45" src="https://github.com/user-attachments/assets/75319c45-712c-4df8-94e2-e1a3bc03c3a1" />

## Requirements
- Create an app on Discord Developer Portal and get token
<img width="1391" height="582" alt="image" src="https://github.com/user-attachments/assets/7dd7e7e4-e40a-42c1-a080-134fe2ff425f" />

- Bot must have `applications.commands` and `bot` scope with required scopes and `Send Messages` and `Read Channels` permissions
<img width="1460" height="570" alt="image" src="https://github.com/user-attachments/assets/a313e3fe-2919-4723-aae6-538bb3a30369" />

<img width="1072" height="762" alt="image" src="https://github.com/user-attachments/assets/72d4abbb-89b1-4a21-b166-b1498fa831dd" />


## Docker Compose (recommended)
- Have Docker installed https://www.docker.com/get-started/
- Create docker-compose.yaml and paste the following below
- ````services:
  discord-gamebot:
    image: ghcr.io/jimmysfedora/random-game-discord-bot:latest
    container_name: discord-gamebot
    restart: unless-stopped
    env_file:
      - .env
    volumes:
      - ./games.csv:/app/games.csv
- Create an `.env` file with TOKEN entry with key from Discord Developer Portal in same directory as compose file
- Create a `games.csv` file in same directory with desired games
- Run `docker compose up -d`
- Verify container is running and no errors with `docker ps` and `docker logs container_id`
- Invite bot to server from OAuth2 link using required permissions

## Python Installation
- Have Python installed
- Clone repo with `git clone https://github.com/jimmysFedora/random-game-discord-bot`
- Invite bot to server from OAuth2 link
- Create an `.env` file with TOKEN entry with key from Discord Developer Portal
- Edit provided `games.csv` with desired games
- Move python file and csv file into the same directory where your environment file is and delete the data and src folders prior to running the script

## Example .env file
```
TOKEN=YOURKEYHERE
```
