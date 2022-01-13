import os
import aiohttp
import asyncio
import discord
from discord.ext import commands
from dotenv import load_dotenv

intents = discord.Intents.default()
intents.members = True
load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')
bot = commands.Bot(command_prefix='>', help_command=None, owner_id="Your owner ID", case_insensitive=True, intents=intents)

for filename in os.listdir('./commands'):
	if filename.endswith('.py'):
		bot.load_extension(f'commands.{filename[:-3]}')
	else:
		print(f'Unable to load {filename[:-3]}')

@bot.event
async def on_ready():
	print("Bot is ready!")
	await bot.change_presence(activity=discord.Game(name="Regular functionality!"))


bot.run(TOKEN)
