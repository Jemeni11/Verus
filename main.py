import random
import os

import discord
from discord.ext import commands
from discord.utils import get
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

@bot.event
async def on_ready():
    print(f"Logged in as {bot.user} (ID: {bot.user.id})")
    print("------")

@bot.command()
async def joined(ctx, member: discord.Member):
    """Says when a member joined."""
    await ctx.send(f"{member.name} joined in {member.joined_at}")

@bot.event
async def on_member_join(member):
  guild = member.guild
  if guild.system_channel is not None:
    to_send = f"Welcome {member.mention} to {guild.name}!"
    await guild.system_channel.send(to_send)
  # channel = get(ctx.guild.channels,name="Welcome")
  # await channel.send(f"{member.mention} has joined")
  new_captcha()
  welcome_message = Embed(
    title=f"{guild.name} Verification Bot",
    description=f"""
      Welcome to {guild.name}, {member.mention}!
      \nWe hope you enjoy your stay here but we need you to complete verification below.
      \nPlease enter the numbers you see in the image.
    """
  )
  try:
    file = discord.File("./output.png")
    welcome_message.set_image(url="attachment://output.png")
    await member.send(file = file, embed=welcome_message)
  except:
    await member.send(embed=welcome_message)

@bot.event
async def on_message(message):
  if message.author.id == bot.user.id:
    return

  if message.author.bot:
    return  #

  if message.content == 'TASK':
    # await member.add_roles(message.author, verify_role)
    await message.channel.send(f'{message.author}, thanks!')

bot.run(BOT_TOKEN)