import discord
from discord.ext import commands
import random

meow=["meow","meow meow I like you!","meowww","hm...meow","meow meow meeeow","meow :3","meow meow meowwwww"]

intents=discord.Intents.all()
bot=commands.Bot("$",intents=intents)

@bot.event
async def on_ready():
  print("The bot is ready meoww")

connect=sqlite3.connect("guilds.db")
cursor=connect.cursor()
cursor.execute("""CREATE TABLE IF NOT EXISTS ids(
               guild_id integer,
               channel_id integer)""")
connect.commit()

@bot.tree.command()
@app_commands.checks.has_permissions(manage_guild=True)#this command will basically allow you to chose that in which channel you want the meow work, like where you will like it to say meow whenever it says anything
async def chosechannel(interaction:discord.Interaction, channel:str):
    if channel.endswith(">") and channel.startswith("<#"):
        channel=channel.replace("<#","")
        channel=channel.replace(">","")
        channel=int(channel)
        guildid=interaction.guild_id
        d={"guild_id":guildid, "channel_id":channel}
        l=[d["guild_id"],d["channel_id"]]
        cursor.execute("INSERT INTO ids VALUES (?,?)",l)
        cursor.execute("SELECT * FROM ids")
        connect.commit()
        line=cursor.fetchall()
        print(line)
        await interaction.response.defer(ephemeral=True)
        await interaction.followup.send("The channel is assigned! You can try that now.")
    else:
        await interaction.response.defer(ephemeral=True)
        await interaction.followup.send("You should just mention a channel to allow")

@bot.event
async def on_message(message:discord.Message):
    if message.author==bot.user:
        return
    else:
        cursor.execute("SELECT * FROM ids")
        line=cursor.fetchall()
        for i in line:
            if message.guild.id==i[0]:
                if message.channel.id==i[1]:
                    channel=message.guild.get_channel(message.channel.id)
                    await channel.send(f"{random.choice(meow)}")
                    break
                else:
                    continue
            else:
                continue
    await bot.process_commands(message)

bot.run("TOKEN")
