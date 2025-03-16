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

bot.run(DISCORD_TOKEN)