import discord
from discord.ext import commands
import sqlite3
import random
from discord import app_commands
import requests

intents=discord.Intents.all()
bot=commands.Bot("$",intents=intents)

colors=[0x000000,0xafafaf,0x12ce6f,0xffffff,0xab92e1,0xfa579e,0xe48ad1,0x32af6c,0xcf5cf5]

connect=sqlite3.connect("tags_list.db")
cursor=connect.cursor()

conn=sqlite3.connect("tags.db")
curs=conn.cursor()
curs.execute("""CREATE TABLE IF NOT EXISTS tag(
             tag_name text,
             link text,
             contributor int)""")

def Tags():
    cursor.execute("SELECT * FROM tag_list")
    info=cursor.fetchall()
    l=[]
    for i in info:
        l.append(i[0])
    return l
def numbers():
    cursor.execute("SELECT * FROM tag_list")
    info=cursor.fetchall()
    l=[]
    for i in info:
        l.append(i[0])
    return l
def Links():
    curs.execute("SELECT link FROM tag")
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
    tags=tags.lower()
    if " " in link:
        link=link.replace(" ","")
    response=requests.get(link)
    if response.status_code==200:
        if "jpg" in link or "jpeg" in link or "png" in link or "webp" in link or "gif" in link:
            curs.execute("INSERT INTO tag VALUES (?,?,?)",[tags.lower(),link,ctx.author.id])
            conn.commit()
            embed=discord.Embed(color=random.choice(colors),description=f"*Thanks for your contribution {ctx.author.mention}*\n*Tag: {tags}*")
            embed.set_image(url=link)
            embed.set_author(name=ctx.author.global_name,icon_url=ctx.author.display_avatar.url)
            await ctx.send(embed=embed)
            number=numbers()
            if tags in number:
                cursor.execute("SELECT * FROM tag_list WHERE tag=?",[tags])
                info=cursor.fetchone()
                print(info)
                n=info[1]
                z=info[0]
                cursor.execute(f"UPDATE tag_list SET number=? WHERE tag=?",[(n+1),z])
                connect.commit()
            else:
                cursor.execute(f"INSERT INTO tag_list VALUES (?,?)",[tags,1])
                connect.commit()
            cursor.execute("SELECT * FROM tag_list")
            info=cursor.fetchall()
            return print(info)
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

@bot.command()
async def call(ctx:commands.Context,tagName:str):
    l=Tags()
    if tagName.lower() in l:
        curs.execute("SELECT * FROM tag WHERE tag_name=?",[tagName])
        data=curs.fetchall()
        img=random.choice(data)
        embed=discord.Embed(color=random.choice(colors))
        embed.set_image(url=img[1])
        embed.set_footer(text=f"Tag: {tagName}")
        return await ctx.send(embed=embed)
    else:
        embed=discord.Embed(color=random.choice(colors),description=f"*No tag named {tagName} found :(*")
        return await ctx.send(embed=embed)
    
@bot.command()
async def kiss(ctx:commands.Context,member:discord.Member|None=None):
    curs.execute(f"SELECT * FROM tag WHERE tag_name=?",[random.choice(["kiss","flyingkiss","flying kiss"])])
    links=curs.fetchall()
    img=random.choice(links)
    if member is not None:
        embed=discord.Embed(color=random.choice(colors),description=f"*{ctx.author.mention} kisses you {member.mention}!!!*")
        embed.set_image(url=img[1])
        await ctx.send(embed=embed)
    else:
        embed=discord.Embed(color=random.choice(colors),description=f"*Kisses you, {ctx.author.mention}*")
        embed.set_image(url=img[1])
        await ctx.send(embed=embed)

@bot.command()
async def heart(ctx:commands.Context,member:discord.Member|None=None):
    curs.execute(f"SELECT * FROM tag WHERE tag_name=?",["heart"])
    links=curs.fetchall()
    img=random.choice(links)
    if member is not None:
        embed=discord.Embed(color=random.choice(colors))
        embed.set_image(url=img[1])
        await ctx.send(embed=embed)
    else:
        embed=discord.Embed(color=random.choice(colors))
        embed.set_image(url=img[1])
        await ctx.send(embed=embed)

@bot.command()
async def tagList(ctx:commands.Context):
    cursor.execute("SELECT * FROM tag_list")
    info=cursor.fetchall()
    desc=""
    for i in info:
        desc+=f"{i[0]} ({i[1]})\n"
    embed=discord.Embed(description=desc,color=random.choice(colors))
    await ctx.send(embed=embed)

@bot.command()
async def Contributor(ctx:commands.Context,link:str):
    l=Links()
    if link in l:
        curs.execute("SELECT * FROM tag WHERE link=?",[link])
        info=curs.fetchone()
        embed=discord.Embed(description=f"Contributor: <@{info[2]}>",color=random.choice(colors))
        embed.set_image(url=link)
        await ctx.send(embed=embed)
    else:
        embed=discord.Embed(description="Not found in our database :(",color=random.choice(colors))
        await ctx.send(embed=embed)

bot.run("TOKEN")

#rebuilding everything from scratch, but it wouldn't take much time
#added one function only replacing two
