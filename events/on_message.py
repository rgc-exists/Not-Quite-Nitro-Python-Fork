from discord.ext import commands
from discord import utils
import discord
import regex

from keys import *
from gemini import *

WHITELISTED_CHANNELS = [1351276068656644096]

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
     
		if message.author.bot:
			return

		if message.channel.id in WHITELISTED_CHANNELS:
			
			print(f"Recieved message: {message.content}")
			try:
				if regex.match("^((?i)\\b((?:https?:(?:/{1,3}|[a-z0-9%])|[a-z0-9.\\-]+[.](?:com|net|org|edu|gov|mil|aero|asia|biz|cat|coop|info|int|jobs|mobi|museum|name|post|pro|tel|travel|xxx|ac|ad|ae|af|ag|ai|al|am|an|ao|aq|ar|as|at|au|aw|ax|az|ba|bb|bd|be|bf|bg|bh|bi|bj|bm|bn|bo|br|bs|bt|bv|bw|by|bz|ca|cc|cd|cf|cg|ch|ci|ck|cl|cm|cn|co|cr|cs|cu|cv|cx|cy|cz|dd|de|dj|dk|dm|do|dz|ec|ee|eg|eh|er|es|et|eu|fi|fj|fk|fm|fo|fr|ga|gb|gd|ge|gf|gg|gh|gi|gl|gm|gn|gp|gq|gr|gs|gt|gu|gw|gy|hk|hm|hn|hr|ht|hu|id|ie|il|im|in|io|iq|ir|is|it|je|jm|jo|jp|ke|kg|kh|ki|km|kn|kp|kr|kw|ky|kz|la|lb|lc|li|lk|lr|ls|lt|lu|lv|ly|ma|mc|md|me|mg|mh|mk|ml|mm|mn|mo|mp|mq|mr|ms|mt|mu|mv|mw|mx|my|mz|na|nc|ne|nf|ng|ni|nl|no|np|nr|nu|nz|om|pa|pe|pf|pg|ph|pk|pl|pm|pn|pr|ps|pt|pw|py|qa|re|ro|rs|ru|rw|sa|sb|sc|sd|se|sg|sh|si|sj|Ja|sk|sl|sm|sn|so|sr|ss|st|su|sv|sx|sy|sz|tc|td|tf|tg|th|tj|tk|tl|tm|tn|to|tp|tr|tt|tv|tw|tz|ua|ug|uk|us|uy|uz|va|vc|ve|vg|vi|vn|vu|wf|ws|ye|yt|yu|za|zm|zw)/)(?:[^\\s()<>{}\\[\\]]+|\\([^\\s()]*?\\([^\\s()]+\\)[^\\s()]*?\\)|\\([^\\s]+?\\))+(?:\\([^\\s()]*?\\([^\\s()]+\\)[^\\s()]*?\\)|\\([^\\s]+?\\)|[^\\s`!()\\[\\]{};:\'\".,<>?«»“”‘’])|(?:(?<!@)[a-z0-9]+(?:[.\\-][a-z0-9]+)*[.](?:com|net|org|edu|gov|mil|aero|asia|biz|cat|coop|info|int|jobs|mobi|museum|name|post|pro|tel|travel|xxx|ac|ad|ae|af|ag|ai|al|am|an|ao|aq|ar|as|at|au|aw|ax|az|ba|bb|bd|be|bf|bg|bh|bi|bj|bm|bn|bo|br|bs|bt|bv|bw|by|bz|ca|cc|cd|cf|cg|ch|ci|ck|cl|cm|cn|co|cr|cs|cu|cv|cx|cy|cz|dd|de|dj|dk|dm|do|dz|ec|ee|eg|eh|er|es|et|eu|fi|fj|fk|fm|fo|fr|ga|gb|gd|ge|gf|gg|gh|gi|gl|gm|gn|gp|gq|gr|gs|gt|gu|gw|gy|hk|hm|hn|hr|ht|hu|id|ie|il|im|in|io|iq|ir|is|it|je|jm|jo|jp|ke|kg|kh|ki|km|kn|kp|kr|kw|ky|kz|la|lb|lc|li|lk|lr|ls|lt|lu|lv|ly|ma|mc|md|me|mg|mh|mk|ml|mm|mn|mo|mp|mq|mr|ms|mt|mu|mv|mw|mx|my|mz|na|nc|ne|nf|ng|ni|nl|no|np|nr|nu|nz|om|pa|pe|pf|pg|ph|pk|pl|pm|pn|pr|ps|pt|pw|py|qa|re|ro|rs|ru|rw|sa|sb|sc|sd|se|sg|sh|si|sj|Ja|sk|sl|sm|sn|so|sr|ss|st|su|sv|sx|sy|sz|tc|td|tf|tg|th|tj|tk|tl|tm|tn|to|tp|tr|tt|tv|tw|tz|ua|ug|uk|us|uy|uz|va|vc|ve|vg|vi|vn|vu|wf|ws|ye|yt|yu|za|zm|zw)\\b/?(?!@))))$", message.content):
					print("Detected link, resending exactly as is.")
					ret = message.content
				elif len(message.content.strip()) <= 0:
					ret = ""
				else:
					ret = await make_pirate_message(message.content)
     
				if ret is None:
					return
 
				username = message.author.nick
				if username is None:
					username = message.author.global_name
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
					await webhook.send(ret, username = username, avatar_url = message.author.avatar, files = files)
      
					await message.delete()
				else:
					print("Pirate-ified message was too long for discord.")
			except Exception as e:
				print(f"An exception occured in on_message:\n{e}")
		else:
			print("Message was not in a whitelisted channel.")
async def setup(bot):
	await bot.add_cog(emoji(bot))