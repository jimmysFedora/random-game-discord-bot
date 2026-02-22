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
    games = read_games()
    
    if not games:
        await interaction.response.send_message("The game list is empty or missing!")
        return

    selected_game = random.choice(games)
    await interaction.response.send_message(f"Doggo recommends **{selected_game}**.")

@bot.tree.command(name="list", description="List all multiplayer games")
async def list_games(interaction: discord.Interaction):
    games = read_games()
    
    if not games:
        await interaction.response.send_message("The game list is empty or missing!")
        return
    formatted_list = "\n".join([f"• {game}" for game in games])

    await interaction.response.send_message(f"**Current Games:**\n{formatted_list}")

bot.run(TOKEN)