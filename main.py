import os

import discord
from discord.ext import commands
from discord import Embed

from captchaGenerator import new_captcha

from dotenv import load_dotenv

load_dotenv()

BOT_TOKEN = os.getenv('TOKEN')

intents = discord.Intents.default()
intents.members = True
# intents.guilds = True
# intents.messages = True
# intents.reactions = True

bot = commands.Bot(command_prefix="?", intents=intents)
count = 3


@bot.event
async def on_ready():
	print(f"Logged in as {bot.user} (ID: {bot.user.id})")
	print("------")


@bot.command()
async def joined(ctx, member: discord.Member):
	"""Says when a member joined."""
	await ctx.send(f"{member.name} joined in {member.joined_at}")


@bot.command()
async def gtn(ctx):
	"""A Slash Command to play a Guess-the-Number game."""

	await ctx.respond('Guess a number between 1 and 10.')
	guess = await bot.wait_for('message', check=lambda message: message.author == ctx.author)

	if int(guess.content) == 5:
		await ctx.send('You guessed it!')
	else:
		await ctx.send('Nope, try again.')


@bot.event
async def on_member_join(member):
	guild = member.guild
	if guild.system_channel is not None:
		to_send = f"Welcome {member.mention} to {guild.name}!"
		await guild.system_channel.send(to_send)
	verification_numbers = new_captcha()
	welcome_message = Embed(
		title=f"{guild.name} Verification Bot",
		description=f"""
		Welcome to {guild.name}, {member.mention}!
		\nWe hope you enjoy your stay here but we need you to complete verification below.
		\nPlease enter the numbers you see in the image."""
	)

	try:
		file = discord.File("./output.png")
		welcome_message.set_image(url="attachment://output.png")
		await member.send(file=file, embed=welcome_message)
	except:
		await member.send(embed=welcome_message)

	@bot.event
	async def on_message(message):
		global count
		if message.author.id == bot.user.id:
			return

		if message.author.bot:
			return  #

		while count != 0:
			msg = message.content == verification_numbers
			if msg:
				# add a verified role that lets the user access the server
				await member.send('Welcome!')
				break
			else:
				error = Embed(
					title="Wrong",
					description=f"{count} chances left"
				)
				await member.send(embed=error)
				count -= 1
		if count == 0:
			await member.send("You have used up all your chances.")
			count = 3

if __name__ == '__main__':
	bot.run(BOT_TOKEN)
