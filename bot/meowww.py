import discord
from discord.ext import commands
import random

meow=["meow","meow meow I like you!","meowww","hm...meow","meow meow meeeow","meow :3","meow meow meowwwww"]

intents=discord.Intents.all()
bot=commands.Bot("$",intents=intents)

@bot.event
async def on_ready():
  print("The bot is ready meoww")

@bot.event
async def on_message(message:discord.Message):
  if message.author==bot.user:
    return
  if message.channel.id==1518594138214371378:#give your channel id where you want the bot to say meow on every message you send
    if "" in message.content:
      channel=message.guild.get_channel(1518594138214371378)#use that channel only
      await channel.send(f"{random.choice(meow)}")
  await bot.proccess_commands(message)#this will allow you to use commands when it's a command call

bot.run("TOKEN")
#i have done it better, like I have made a whole embed with random images, but I am scared of copyrights of the image here, so I am not using that here, but you can look at my channel and server
#and this may look spammy, but i have filled random, and we will try to give a cooldown, events can't make cooldown unless it is cog, but we will use sqlite3 for that later ^^
