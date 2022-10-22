#https://discord.com/api/oauth2/authorize?client_id=1032752693564944474&permissions=1634235578432&scope=bot
import discord
import responses

async def send_message(message, user_message, is_private, attachments):
	try:
		respone = None
		if attachments:
			response = responses.handle_response(user_message, attachments[0].url)
		else:
			response = responses.handle_response(user_message, None)
		if response == None:
			return
		await message.author.send(response) if is_private else await message.channel.send(response)
	except Exception as e:
		raise e
		#print(e)

def run_discord_bot():
	TOKEN = '<DISCORD BOT TOKEN HERE>'
	client = discord.Client()

	@client.event
	async def on_ready():
		print(f'{client.user} is now running!')

	@client.event
	async def on_message(message):
		if message.author == client.user:
			return

		username = str(message.author)
		user_message = str(message.content)
		channel = str(message.channel)

		if message.attachments:
			print(f"{username} sent an attachment: '{message.attachments[0].url}' ({channel})")

		#print(f"{username} said: '{user_message}' ({channel})")

		if len(user_message) <= 0:
			return

		if user_message[0] == '?':
			user_message == user_message[1:]
			await send_message(message, user_message, is_private=True, attachments=message.attachments)
		else:
			await send_message(message, user_message, is_private=False, attachments=message.attachments)

	client.run(TOKEN)