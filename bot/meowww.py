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

bot.run("TOKEN")

#rebuilding everything from scratch, but it wouldn't take much time
