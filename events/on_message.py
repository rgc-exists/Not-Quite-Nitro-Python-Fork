from discord.ext import commands
from discord import utils
import discord

from keys import *
from gemini import *

BLACKLISTED_CHANNELS = [1350195999615881286, 1350196046361526512]

class emoji(commands.Cog):
	def __init__(self, bot):
		self.bot = bot

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



	@commands.Cog.listener()
	async def on_message(self, message):
		print(f"Recieved message: {message.content}")
     
		if message.author.bot:
			return

		if not message.channel.id in BLACKLISTED_CHANNELS:
			
			try:
				ret = await make_pirate_message(message.content)

				username = message.author.nick
				if username is None:
					username = message.author.global_name
				print(f"\n\nusername/nickname:{username}")
       
				webhooks = await message.channel.webhooks()
				webhook = utils.get(webhooks, name = "Imposter NQN")
				if webhook is None:
					webhook = await message.channel.create_webhook(name = "Imposter NQN")
				
				if len(ret) < 2000:
					await webhook.send(ret, username = username, avatar_url = message.author.avatar)
					await message.delete()
				else:
					print("Pirate-ified message was too long for discord.")
			except Exception as e:
				print(f"An exception occured in on_message:\n{e}")

async def setup(bot):
	await bot.add_cog(emoji(bot))