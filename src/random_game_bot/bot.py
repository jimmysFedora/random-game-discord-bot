import csv
import logging
import os
import sqlite3
from pathlib import Path

import discord
from discord import app_commands
from dotenv import load_dotenv

log = logging.getLogger(__name__)


# --- Database ---
def connect(path: Path) -> sqlite3.Connection:
    """Open the database, creating it and importing a sibling games.csv if it's empty."""
    path.parent.mkdir(parents=True, exist_ok=True)
    db = sqlite3.connect(path)
    db.execute(
        "CREATE TABLE IF NOT EXISTS games ("
        "id INTEGER PRIMARY KEY, "
        "name TEXT NOT NULL UNIQUE COLLATE NOCASE)"
    )
    seed_csv = path.with_name("games.csv")
    empty = db.execute("SELECT 1 FROM games LIMIT 1").fetchone() is None
    if empty and seed_csv.exists():
        with open(seed_csv, newline="") as f:
            rows = [(row[0].strip(),) for row in csv.reader(f) if row and row[0].strip()]
        db.executemany("INSERT OR IGNORE INTO games (name) VALUES (?)", rows)
        log.info("Imported %d games from %s", len(rows), seed_csv)
    db.commit()
    return db


# --- Helpers ---
def chunk_lines(lines: list[str], limit: int = 2000) -> list[str]:
    """Group lines into messages that fit Discord's character limit."""
    chunks, current = [], ""
    for line in lines:
        if current and len(current) + 1 + len(line) > limit:
            chunks.append(current)
            current = line
        else:
            current = f"{current}\n{line}" if current else line
    chunks.append(current)
    return chunks


# --- Bot ---
class Bot(discord.Client):
    def __init__(self):
        super().__init__(intents=discord.Intents.default())
        self.tree = app_commands.CommandTree(self)

    async def setup_hook(self):
        await self.tree.sync()

    async def on_ready(self):
        log.info("Logged in as %s (ID: %s)", self.user, self.user.id)


def create_bot(db: sqlite3.Connection) -> Bot:
    bot = Bot()

    @bot.tree.command(name="roll", description="Pick a random game from the list")
    async def roll(interaction: discord.Interaction):
        row = db.execute("SELECT name FROM games ORDER BY RANDOM() LIMIT 1").fetchone()
        if row is None:
            await interaction.response.send_message("The game list is empty.")
            return
        await interaction.response.send_message(f"**{row[0]}**")

    @bot.tree.command(name="list", description="List all games")
    async def list_games(interaction: discord.Interaction):
        games = [r[0] for r in db.execute("SELECT name FROM games ORDER BY name COLLATE NOCASE")]
        if not games:
            await interaction.response.send_message("The game list is empty.")
            return
        chunks = chunk_lines([f"- {g}" for g in games])
        await interaction.response.send_message(chunks[0])
        for chunk in chunks[1:]:
            await interaction.followup.send(chunk)

    @bot.tree.command(name="add", description="Add a game to the list")
    async def add_game(interaction: discord.Interaction, game: app_commands.Range[str, 1, 100]):
        game = game.strip()
        with db:
            cur = db.execute("INSERT OR IGNORE INTO games (name) VALUES (?)", (game,))
        if cur.rowcount == 0:
            await interaction.response.send_message(f"**{game}** is already in the list.")
            return
        log.info("Added '%s'", game)
        await interaction.response.send_message(f"Added **{game}**.")

    @bot.tree.command(name="rm", description="Remove a game from the list")
    async def remove_game(interaction: discord.Interaction, game: str):
        game = game.strip()
        with db:
            row = db.execute("DELETE FROM games WHERE name = ? RETURNING name", (game,)).fetchone()
        if row is None:
            await interaction.response.send_message(f"**{game}** is not in the list.")
            return
        log.info("Removed '%s'", row[0])
        await interaction.response.send_message(f"Removed **{row[0]}**.")

    @remove_game.autocomplete("game")
    async def remove_game_autocomplete(interaction: discord.Interaction, current: str):
        rows = db.execute(
            "SELECT name FROM games WHERE instr(lower(name), lower(?)) > 0 "
            "ORDER BY name COLLATE NOCASE LIMIT 25",
            (current,),
        )
        return [app_commands.Choice(name=r[0], value=r[0]) for r in rows]

    return bot


def main():
    discord.utils.setup_logging(root=True)
    load_dotenv()
    token = os.getenv("TOKEN")
    if not token:
        raise SystemExit("TOKEN is not set. Add it to .env or the environment.")
    db = connect(Path(os.getenv("DB_PATH", "data/games.db")))
    create_bot(db).run(token, log_handler=None)
