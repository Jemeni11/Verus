import random
import os

import discord
from discord.ext import commands
from discord.utils import get

from dotenv import load_dotenv

load_dotenv() 

BOT_TOKEN = os.getenv('TOKEN')

intents = discord.Intents.default()
intents.members = True

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
  # channel = get(ctx.guild.channels,name="Welcome")
  # await channel.send(f"{member.mention} has joined")
  await member.send(f'Welcome to the server, {member.mention}! Enjoy your stay here.\nSend a **TASK**')

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