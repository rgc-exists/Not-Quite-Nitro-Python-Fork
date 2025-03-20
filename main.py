import traceback

from discord.ext import commands
import discord

from keys import *

intents = discord.Intents.all()
bot = commands.Bot(command_prefix = ".", intents = intents)
cogs = ["events.on_message"]

@bot.event
async def on_ready():
	print("The bot is ready!")
	for cog in cogs:

		await bot.load_extension(cog)
		print(f"{cog} was loaded.")

@bot.event
async def on_error(event, *args, **kwargs):
	print(f"Error in {event}:")
	traceback.print_exc()

bot.run(DISCORD_TOKEN)
