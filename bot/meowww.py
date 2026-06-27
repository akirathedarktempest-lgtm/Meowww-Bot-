import discord
from discord.ext import commands
import sqlite3
import random
from discord import app_commands

connect=sqlite3.connect("guild.db")
cursor=connect.cursor()

cursor.execute("""CREATE TABLE IF NOT EXISTS ids(
               guild_id integer,
               channel_id str)""")

intents=discord.Intents.all()
bot=commands.Bot("$",intents=intents)

def GuildData():
    cursor.execute("SELECT guild_id FROM ids")
    info=cursor.fetchall()
    l=[]
    for i in info:
        l.append(i[0])
    return l
def ChannelData():
    cursor.execute("SELECT channel_id FROM ids")
    info=cursor.fetchall()
    l=[]
    for i in info:
        l.append(i[0])
    return l

@bot.event
async def on_ready():
    print(f"The {bot.user} is ready!")
    await bot.tree.sync()

@bot.tree.command(name="choose")
@app_commands.checks.has_permissions(manage_guild=True)
async def choose(interaction:discord.Interaction,channel:str):
    await interaction.response.defer(ephemeral=True)
    cursor.execute("SELECT * FROM ids")
    info=cursor.fetchall()
    for i in info:
        if i[0]==interaction.guild.id:
            if channel.startswith("<#") and channel.endswith(">"):
                channel=channel.rstrip(">")
                channel=channel.lstrip("<#")
                try:
                    channel=int(channel)
                    cursor.execute(f"UPDATE ids SET channel_id=? WHERE guild_id={interaction.guild.id}",[f"{str(channel)}-"])
                    connect.commit()
                    return await interaction.followup.send(f"The <#{channel}> has been assigned!")
                except ValueError as e:
                    print(e)
                    return await interaction.followup.send("Please send a proper channel mention only")
            else:
                return await interaction.followup.send("Please send a proper channel mention only")
        else:
            print("Checking line 43")
    if channel.startswith("<#") and channel.endswith(">"):
        channel=channel.rstrip(">")
        channel=channel.lstrip("<#")
        try:
            channel=int(channel)
            cursor.execute("INSERT INTO ids VALUES (?,?)",[interaction.guild.id,f"{channel}-"])
            connect.commit()
            await interaction.followup.send(f"The <#{channel}> has been assigned!")
            return
        except ValueError as e:
            print(e)
            return await interaction.followup.send("Please send a proper channel mention only")
    else:
        return await interaction.followup.send("Please send a proper channel mention only")
    
@bot.event
async def on_message(message:discord.Message):
    guild=GuildData()
    channel=ChannelData()
    if message.author==bot.user:
        return
    if message.guild.id in guild:
        number=guild.index(message.guild.id)
        channel_ids=channel[number]
        channel_ids=channel_ids.split("-")
        for i in channel_ids:
            if message.channel.id==int(i):
                channels=message.guild.get_channel(int(i))
                await channels.send(random.choice(["meow","meowww","meow ;3","meow :3"]))
                break
            else:
                pass
    await bot.process_commands(message)

bot.run("TOKEN")

#rebuilding everything from scratch, but it wouldn't take much time
#added two functions which will take care of making lists of guild id and channel id
#you may think, then it can be a problem at indexing? well, most probably it shouldn't, because the indexing of GuildData and ChannelData will be same, it depends on database
#and the guild id wouldn't have empty channels, because the guild id is only added when you are also adding its channel id, if the guild id already exist in db, channel id will be added, if not then it will be created
