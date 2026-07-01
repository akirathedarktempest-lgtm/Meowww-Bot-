import discord
from discord.ext import commands
import sqlite3
import random
from discord import app_commands
import requests

intents=discord.Intents.all()
bot=commands.Bot("$",intents=intents)

colors=[0x000000,0xafafaf,0x12ce6f,0xffffff,0xab92e1,0xfa579e,0xe48ad1,0x32af6c,0xcf5cf5]

conn=sqlite3.connect("tags.db")
curs=conn.cursor()
curs.execute("""CREATE TABLE IF NOT EXISTS tag(
             tag_name text,
             link text,
             contributor int)""")

def Tags():
    curs.execute("SELECT * FROM tag")
    info=curs.fetchall()
    l=[]
    for i in info:
        l.append(i[0])
    return l

@bot.event
async def on_ready():
    print(f"{bot.user} is online!")
    await bot.tree.sync()

@bot.command()
async def tag(ctx:commands.Context,tags:str,link:str):
    if " " in link:
        link=link.replace(" ","")
    response=requests.get(link)
    if response.status_code==200:
        if "jpg" in link or "jpeg" in link or "png" in link or "webp" in link or "gif" in link:
            curs.execute("INSERT INTO tag VALUES (?,?,?)",[tags,link,ctx.author.id])
            conn.commit()
            embed=discord.Embed(color=random.choice(colors),description=f"*Thanks for your contribution {ctx.author.mention}*\n*Tag: {tags}*")
            embed.set_image(url=link)
            embed.set_author(name=ctx.author.global_name,icon_url=ctx.author.display_avatar.url)
            return await ctx.send(embed=embed)
    await ctx.send("Invalid link :(\n-# Suggestion, look at the links which have words like jpg, jpeg, png, webp, gif, these extension supports images and no other extensions are valid here")
    

@bot.command()
async def hugs(ctx:commands.Context,member:discord.Member|None=None):
    curs.execute(f"SELECT * FROM tag WHERE tag_name=?",["hug"])
    links=curs.fetchall()
    img=random.choice(links)
    if member is not None:
        embed=discord.Embed(color=random.choice(colors),description=f"*Hugs you {member.mention}!!!*")
        embed.set_image(url=img[1])
        await ctx.send(embed=embed)
    else:
        embed=discord.Embed(color=random.choice(colors),description=f"*Hugs you {ctx.author.mention}*")
        embed.set_image(url=img[1])
        await ctx.send(embed=embed)

bot.run("TOKEN")

#rebuilding everything from scratch, but it wouldn't take much time
#added one function only replacing two
