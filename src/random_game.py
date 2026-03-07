import discord
from discord import app_commands

# load api token from .env MAKE sure u have TOKEN=EXAMPLESTRINGWITHOUTQUOTES
import os
from dotenv import load_dotenv
load_dotenv()

# make sure csv entries have no commas
import random
import csv

# --- Configuration ---
FILENAME = "games.csv"

TOKEN = os.getenv("TOKEN")
def read_games():
    try:
        with open(FILENAME, newline="") as file:
            reader = csv.reader(file)
            return [row[0] for row in reader if row]
    except FileNotFoundError:
        return []

# --- Bot Setup ---
class MyBot(discord.Client):
    def __init__(self):
        # Intents define what data your bot can see
        intents = discord.Intents.default()
        super().__init__(intents=intents)
        self.tree = app_commands.CommandTree(self)

    async def setup_hook(self):
        # This syncs your slash commands with Discord
        await self.tree.sync()

bot = MyBot()

@bot.event
async def on_ready():
    print(f'Logged in as {bot.user} (ID: {bot.user.id})')
    print('------')

# --- Commands ---

@bot.tree.command(name="roll", description="Pick a random game from the list")
async def roll(interaction: discord.Interaction):
    games = sorted(read_games(), key=str.casefold)
    
    if not games:
        await interaction.response.send_message("Doggo lost the game list. 💀 Doggo recommends checking if games.csv exists")
        return

    selected_game = random.choice(games)
    await interaction.response.send_message(f"Doggo recommends **{selected_game}**.")

@bot.tree.command(name="list", description="List all multiplayer games")
async def list_games(interaction: discord.Interaction):
    games = sorted(read_games(), key=str.casefold)
    
    if not games:
        await interaction.response.send_message("Doggo lost the game list. 💀 Doggo recommends checking if games.csv exists")
        return
    formatted_list = "\n".join([f"• {game}" for game in games])

    await interaction.response.send_message(f"**Current Games:**\n{formatted_list}")

@bot.tree.command(name="add", description="Add a game to the list")
async def add_game(interaction: discord.Interaction, game: str):
    games = read_games()
    if game.lower() in [g.lower() for g in games]:
        print(f"Detected duplicate entry '{game}'. Not adding to list")
        await interaction.response.send_message(f"Doggo already has {game} in the list")
        return

    with open(FILENAME, "a", newline="") as file:
        writer = csv.writer(file)
        writer.writerow([game])
        print(f"Added '{game}' as entry into games.csv")
    await interaction.response.send_message(f"Doggo added **{game}** to the list!")

@bot.tree.command(name="rm", description="Removes a game from the list")
async def remove_game(interaction: discord.Interaction, game: str):
    games = read_games()

    if game not in games:
        print(f"'{game}' not detected in list for removal.")
        await interaction.response.send_message(f"Doggo doesn't detect **{game}** in the list. Stop gaslighting.")
        return

    games.remove(game)

    with open(FILENAME, "w", newline="") as file:
        writer = csv.writer(file)
        for deleted_game in games:
            writer.writerow([deleted_game])
    print(f"Removed '{game}' entry from games.csv")
    await interaction.response.send_message(f"Doggo removed **{game}** from the list.")

# Enable webhooks for testing discord server (non-sensitive id)
# async def setup_hook(self):
#     guild = discord.Object(id=1341849279836459108)
#     self.tree.copy_global_to(guild=guild)
#     await self.tree.sync(guild=guild)

bot.run(TOKEN)