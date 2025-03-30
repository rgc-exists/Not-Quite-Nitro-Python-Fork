from urllib.parse import urlparse
from discord.ext import commands
from discord import utils
import discord
from random import random

from keys import *
from gemini import *

WHITELISTED_CHANNELS = [1351276068656644096]

class emoji(commands.Cog):
	def __init__(self, bot):
		self.bot = bot
		self.chance = 0.0

	async def getemote(self, arg):
		emoji = utils.get(self.bot.emojis, name = arg.strip(":"))

		if emoji is not None:
			if emoji.animated:
				add = "a"
			else:
				add = ""
			return f"<{add}:{emoji.name}:{emoji.id}>"
		else:
			return None

	async def getinstr(self, content):
		ret = []

		spc = content.split(" ")
		cnt = content.split(":")

		if len(cnt) > 1:
			for item in spc:
				if item.count(":") > 1:
					wr = ""
					if item.startswith("<") and item.endswith(">"):
						ret.append(item)
					else:
						cnt = 0
						for i in item:
							if cnt == 2:
								aaa = wr.replace(" ", "")
								ret.append(aaa)
								wr = ""
								cnt = 0

							if i != ":":
								wr += i
							else:
								if wr == "" or cnt == 1:
									wr += " : "
									cnt += 1
								else:
									aaa = wr.replace(" ", "")
									ret.append(aaa)
									wr = ":"
									cnt = 1

						aaa = wr.replace(" ", "")
						ret.append(aaa)
				else:
					ret.append(item)
		else:
			return content

		return ret

	async def apply_emotes(self, message):
		msg = await self.getinstr(message)
		ret = ""
		em = False
		smth = message.split(":")
		if len(smth) > 1:
			for word in msg:
				if word.startswith(":") and word.endswith(":") and len(word) > 1:
					emoji = await self.getemote(word)
					if emoji is not None:
						em = True
						ret += f" {emoji}"
					else:
						ret += f" {word}"
				else:
					ret += f" {word}"

		else:
			ret += msg
		return ret
	
	@commands.has_guild_permissions(manage_channels=True)
	@commands.command()
	async def setchance(self, ctx: commands.Context, chance: commands.Range[float, 0.0, 1.0]):
		if ctx.channel.id in WHITELISTED_CHANNELS:
			return
		self.chance = chance
		await ctx.reply(f"Set chance to {self.chance}")
		
	@commands.Cog.listener()
	async def on_message(self, message):
		if message.author.bot:
			return
		
		if message.channel.id in WHITELISTED_CHANNELS:
			if random() > self.chance:
				return
			print(f"Recieved message: {message.content}")
			try:
				parsed = urlparse(message.content)
				ret = message.content if parsed.scheme and parsed.netloc else False
			except:
				ret = False

			if not ret:
				if len(message.content.strip()) <= 0:
					return
				ret = await make_pirate_message(message.content)
				ret = await self.apply_emotes(ret)
    
			username = message.author.nick or message.author.global_name

			print(f"\n\nusername/nickname:{username}")

			ctx = await self.bot.get_context(message)

			reference = message.reference
			if reference is not None:
				reference_message = await ctx.channel.fetch_message(ctx.message.reference.message_id)
				ret = f"""{reference_message.author.name} said: {reference_message.jump_url}
> {reference_message.content.replace("\n", "   ")}
\n""" + ret

			files = [await attachment.to_file() for attachment in message.attachments] 


			webhooks = await message.channel.webhooks()
			webhook = utils.get(webhooks, name = "Imposter NQN")
			if webhook is None:
				webhook = await message.channel.create_webhook(name = "Imposter NQN")


			if len(ret) < 1999:
				await webhook.send(ret, username = username, avatar_url = message.author.avatar, files = files, silent=True, allowed_mentions=discord.AllowedMentions(everyone=False, users=True, roles=False))

				await message.delete()
			else:
				print("Pirate-ified message was too long for discord.")
		else:
			print("Message was not in a whitelisted channel.")
async def setup(bot):
	await bot.add_cog(emoji(bot))
