import asyncio
import discord
import json
import math
import os
import random
import re
import requests
import time
import wikia
import wikipedia
from datetime import datetime
from discord.ext import commands
import xml.etree.ElementTree as ElementTree
client = commands.Bot(command_prefix='!', help_command=None)

def keys_exists(element, *keys):
    if not isinstance(element, dict):
        raise AttributeError('keys_exists() expects dict as first argument.')
    if len(keys) == 0:
        raise AttributeError('keys_exists() expects at least two arguments, one given.')
    _element = element
    for key in keys:
        try:
            _element = _element[key]
        except KeyError:
            return False
    return True
    
embedtimeout = discord.Embed(title='Process Failed')
embedtimeout.add_field(name='Reason', value='Timeout', inline=False)

embedvalueerror = discord.Embed(title='Process Failed')
embedvalueerror.add_field(name='Reason', value='Value Error', inline=False)

# Dice Roll
@client.command(name='roll')
async def roll(ctx, arg1):
    userid = ctx.author.id
    user = client.get_user(userid)
    try:
        if arg1 == "0":
            await ctx.send("Please enter a number greater than 0.")
        else:
            max = int(arg1)
            randno = random.randint(1, max)
            embedrandom = discord.Embed(title=user.name)
            embedrandom.add_field(name='Roll', value=randno, inline=True)
            await ctx.send(embed=embedrandom)
    except ValueError:
        await ctx.send(embed=embedvalueerror)

# Wikipedia
@client.command(name='wikipedia')
async def testes(ctx):
    channel = client.get_channel(664615244236062727)
    try:
        await channel.send("What article would you like to read?")
        await client.wait_for('message', timeout=60)
    except asyncio.TimeoutError:
        await channel.send("too late.")
    else:
        async for message in channel.history(limit=1):
            if message.author == ctx.message.author:
                search = wikipedia.search(message.content)
                try:
                    realpage = search[0]
                except IndexError:
                    await channel.send("Page does not exist.")
                else:
                    page = wikipedia.page(realpage)
                    summary = page.summary
                    title = page.title
                    url = page.url
                    embedwikipedia = discord.Embed(title=title, description=summary, url=url)
                    await channel.send(embed=embedwikipedia)

# TUF Wiki
@client.command(name='wiki')
async def test(ctx):
    channel = client.get_channel(664615244236062727)
    await channel.send("What article would you like to read?")
    try:
        await client.wait_for('message', timeout=60)
    except asyncio.TimeoutError:
        await channel.send("Too late.")
    else:
        async for message in channel.history(limit=1):
            if message.author == ctx.message.author:
                search = wikia.search("the-united-federations", message.content)
                try:
                    realpage = search[0]
                except IndexError:
                    await channel.send("Page does not exist.")
                else:
                    page = wikia.page("the-united-federations", realpage)
                    summary = page.summary
                    title = page.title
                    url = page.url
                    urlword = url.replace(" ", "_")
                    embedwikia = discord.Embed(title=title, description=summary, url=urlword)
                    await channel.send(embed=embedwikia)

# Add/Remove Roles
@client.command(name='role')
async def role(ctx, arg1, arg2):
    user = ctx.message.author
    if arg1 == "add":
        if arg2 == "dead":
            await user.add_roles(discord.utils.get(user.guild.roles, name='Dead, but hidden'))
            await ctx.send("Role given!")
        elif arg2 == "map":
            await user.add_roles(discord.utils.get(user.guild.roles, name='map editor'))
            await ctx.send("Role given!")
        elif arg2 == "anime":
            await user.add_roles(discord.utils.get(user.guild.roles, name='#Anime'))
            await ctx.send("Role given!")
        elif arg2 == "shb":
            await user.add_roles(discord.utils.get(user.guild.roles, name='SHB'))
            await ctx.send("Role given!")
        elif arg2 == "na":
            await user.add_roles(discord.utils.get(user.guild.roles, name='Nova Aeterna'))
            await ctx.send("Role given!")
        elif arg2 == "nrp":
            await user.add_roles(discord.utils.get(user.guild.roles, name='norrpakten'))
            await ctx.send("Role given!")
        elif arg2 == "gl":
            await user.add_roles(discord.utils.get(user.guild.roles, name='GL'))
            await ctx.send("Role given!")
        elif arg2 == "ec":
            await user.add_roles(discord.utils.get(user.guild.roles, name='Eternal Cosmos'))
            await ctx.send("Role given!")
        else:
            await ctx.send("Invalid role.")
    elif arg1 == "remove":
        if arg2 == "dead":
            await user.remove_roles(discord.utils.get(user.guild.roles, name='Dead, but hidden'))
            await ctx.send("Role removed!")
        elif arg2 == "map":
            await user.remove_roles(discord.utils.get(user.guild.roles, name='map editor'))
            await ctx.send("Role removed!")
        elif arg2 == "anime":
            await user.remove_roles(discord.utils.get(user.guild.roles, name='#Anime'))
            await ctx.send("Role removed!")
        elif arg2 == "shb":
            await user.remove_roles(discord.utils.get(user.guild.roles, name='SHB'))
            await ctx.send("Role removed!")
        elif arg2 == "na":
            await user.remove_roles(discord.utils.get(user.guild.roles, name='Nova Aeterna'))
            await ctx.send("Role removed!")
        elif arg2 == "nrp":
            await user.remove_roles(discord.utils.get(user.guild.roles, name='norrpakten'))
            await ctx.send("Role removed!")
        elif arg2 == "gl":
            await user.remove_roles(discord.utils.get(user.guild.roles, name='GL'))
            await ctx.send("Role removed!")
        elif arg2 == "ec":
            await user.remove_roles(discord.utils.get(user.guild.roles, name='Eternal Cosmos'))
            await ctx.send("Role removed!")
        else:
            await ctx.send("Invalid role.")
    else:
        await ctx.send("""Invalid role. Obtainable roles:
[dead]  Dead, but hidden
[map]   map editor
[anime] #Anime
[shb]   SHB
[na]    Nova Aeterna
[nrp]   norrpakten
[gl]    GL
[ec]    Eternal Cosmos""")

# Suggest
@client.command(name='suggest')
async def suggest(ctx):
    channel = client.get_channel(664615244236062727)
    user = ctx.message.author
    userid = ctx.author.id
    try:
        await channel.send("Please give a brief description of the problem.")
        await client.wait_for('message', timeout=60)
    except asyncio.TimeoutError:
        await channel.send(embed=embedtimeout)
    else:
        async for message in channel.history(limit=1):
            if message.author == user:
                problem = message.content
                try:
                    await channel.send("Please provide details regarding the problem.")
                    await client.wait_for('message', timeout=60)
                except asyncio.TimeoutError:
                    await channel.send(embed=embedtimeout)
                else:
                    async for message in channel.history(limit=1):
                        if message.author == user:
                            details = message.content
                            try:
                                await channel.send("Please propose a solution.")
                                await client.wait_for('message', timeout=60)
                            except asyncio.TimeoutError:
                                await channel.send(embed=embedtimeout)
                            else:
                                async for message in channel.history(limit=1):
                                    if message.author == user:
                                        solution = message.content
                                        await channel.send("Process complete.")
                                        embedsuggest = discord.Embed(title='Suggestion', description="Author: <@{}>".format(userid))
                                        embedsuggest.add_field(name="Problem", value=problem, inline=False)
                                        embedsuggest.add_field(name="Details", value=details, inline=False)
                                        embedsuggest.add_field(name="Solution", value=solution, inline=False)
                                        channel = client.get_channel(666213834675060749)
                                        await channel.send(embed=embedsuggest)

# Ships and Fleets
channel1available = True
channel2available = True
channel3available = True

@client.command(name='create')
async def create(ctx):
    global channel1available
    global channel2available
    global channel3available
    user = ctx.message.author
    userid = ctx.author.id
    canrun = None
    if channel1available == True:
        channel1available = False
        channel = client.get_channel(764017189279236096)
        role1 = 'tufbot 1' #role to add
        await user.add_roles(discord.utils.get(user.guild.roles, name=role1))
        canrun = True
    elif channel2available == True:
        channel2available = False
        channel = client.get_channel(764017265125228544)
        role2 = 'tufbot 2' #role to add
        await user.add_roles(discord.utils.get(user.guild.roles, name=role2))
        canrun = True
    elif channel3available == True:
        channel3available = False
        channel = client.get_channel(764017300424622100)
        role3 = 'tufbot 3' #role to add
        await user.add_roles(discord.utils.get(user.guild.roles, name=role3))
        canrun = True
    else:
        await ctx.send("All channels are currently unavailable. Please try again later.")
    while canrun == True:
        try:
            await channel.send("<@{}>, please move here. What would you like to create? (nation/ship/fleet)".format(userid))
            await client.wait_for('message', timeout=60)
        except asyncio.TimeoutError:
            await channel.send(embed=embedtimeout)
            canrun = False
        else:
            async for message in channel.history(limit=1):
                if message.content == "nation" and message.author == user:
                    try:
                        await channel.send("What is the name of the nation?")
                        await client.wait_for('message', timeout=60)
                    except asyncio.TimeoutError:
                        await channel.send(embed=embedtimeout)
                        canrun = False
                    else:
                        async for message in channel.history(limit=1):
                            if message.author == user:
                                filename = message.content + ".txt"
                                nationname = message.content
                                # check if nation exists: if false, proceed
                                try:
                                    f = open(filename)
                                    f.close()
                                except FileNotFoundError:
                                    nationfile = open(filename,"w+")
                                    nation = {"ships":{}, "fleets":{}, "location":{}, "userid":userid}
                                    json.dump(nation, nationfile)
                                    await channel.send("{} has been created.".format(nationname))
                                    nationfile.close()
                                    canrun = False
                                else:
                                    await channel.send("A nation with this name already exists.")
                                    canrun = False
                elif message.content == "ship" and message.author == user:
                    try:
                        await channel.send("Please enter the name of the nation that you want to create the ship in.")
                        await client.wait_for('message', timeout=60)
                    except asyncio.TimeoutError:
                        await channel.send(embed=embedtimeout)
                        canrun = False
                    else:
                        async for message in channel.history(limit=1):
                            nationname = message.content
                            nationfile = message.content + ".txt"
                            # if nation exists: true, proceed
                            try:
                                f = open(nationfile)
                                f.close()
                            except FileNotFoundError:
                                await channel.send("That nation does not exist.")
                                canrun = False
                            else:
                                with open(nationfile) as json_file:
                                    nation = json.load(json_file)
                                if nation["userid"] == userid:
                                    try:
                                        await channel.send("Please enter the name of the ship.")
                                        await client.wait_for('message', timeout=60)
                                    except asyncio.TimeoutError:
                                        await channel.send(embed=embedtimeout)
                                        canrun = False
                                    else:
                                        async for message in channel.history(limit=1):
                                            if message.author == user:
                                                shipname = message.content
                                                # if ship exists, false: proceed
                                                if keys_exists(nation, "ships", shipname):
                                                    await channel.send("You have already created a ship with that name.")
                                                    canrun = False
                                                else:
                                                    await channel.send("Ship's name has been set to {}".format(shipname))
                                                    await channel.send("Please choose a class.")
                                                    embedclasslist = discord.Embed(title='List of Ship Classes', description='Please enter the number next to the class of your choice.')
                                                    embedclasslist.add_field(name="Classifications", value="""1: Striker
2: Corvette
3: Frigate
4: Destroyer
5: Cruiser
6: Battlecruiser
7: Battleship
8: Light Carrier
9: Dreadnaught
10: Carrier
11: Battlesphere
12: Battleglobe""", inline=False)
                                                    try:
                                                        await channel.send(embed=embedclasslist)
                                                        await client.wait_for('message', timeout=60)
                                                    except asyncio.TimeoutError:
                                                        await channel.send(embed=embedtimeout)
                                                        canrun = False
                                                    else:
                                                        async for message in channel.history(limit=1):
                                                            classchoice = message.content
                                                            if message.author == user:
                                                                if int(classchoice) > 12:
                                                                        await channel.send("That is not a valid option.")
                                                                        canrun = False
                                                                else:
                                                                    if classchoice == "1": 
                                                                        shipclass = 'Striker'
                                                                        maxpoints = 30
                                                                        healthmod = 0.4
                                                                        speedmod = (((- (1/30) * math.log(30) + 2000 * (5 / 30)) - 100) / 100) + 1
                                                                        defencemod = 0.5
                                                                        closemod = 2
                                                                        medmod = 0
                                                                        longmod = 0
                                                                        await channel.send("{}'s class has been set to striker.".format(shipname))
                                                                    if classchoice == "2": 
                                                                        shipclass = 'Corvette'
                                                                        maxpoints = 60
                                                                        healthmod = 0.5
                                                                        speedmod = (((- (1/60) * math.log(60) + 2000 * (5 / 60)) - 100) / 100) + 1
                                                                        defencemod = 0.7
                                                                        closemod = 1.8
                                                                        medmod = 0
                                                                        longmod = 0
                                                                        await channel.send("{}'s class has been set to corvette.".format(shipname))
                                                                    if classchoice == "3": 
                                                                        shipclass = 'Frigate'
                                                                        maxpoints = 80
                                                                        healthmod = 0.7
                                                                        speedmod = (((- (1/80) * math.log(80) + 2000 * (5 / 80)) - 100) / 100) + 1
                                                                        defencemod = 0.9
                                                                        closemod = 1.7
                                                                        medmod = 0
                                                                        longmod = 0
                                                                        await channel.send("{}'s class has been set to frigate.".format(shipname))
                                                                    if classchoice == "4": 
                                                                        shipclass = 'Destroyer'
                                                                        maxpoints = 140
                                                                        healthmod = 0.8
                                                                        speedmod = (((- (1/140) * math.log(140) + 2000 * (5 / 140)) - 100) / 100) + 1
                                                                        defencemod = 1
                                                                        closemod = 1.6
                                                                        medmod = 0.7
                                                                        longmod = 0
                                                                        await channel.send("{}'s class has been set to destroyer.".format(shipname))
                                                                    if classchoice == "5":
                                                                        shipclass = 'Cruiser'
                                                                        maxpoints = 310
                                                                        healthmod = 1
                                                                        speedmod = (((- (1/310) * math.log(310) + 2000 * (5 / 310)) - 100) / 100) + 1
                                                                        defencemod = 1.2
                                                                        closemod = 1.4
                                                                        medmod = 1
                                                                        longmod = 0
                                                                        await channel.send("{}'s class has been set to cruiser.".format(shipname))
                                                                    if classchoice == "6": 
                                                                        shipclass = 'Battlecruiser'
                                                                        maxpoints = 970
                                                                        healthmod = 1.1
                                                                        speedmod = (((- (1/970) * math.log(970) + 2000 * (5 / 970)) - 100) / 100) + 1
                                                                        defencemod = 1.4
                                                                        closemod = 1.3
                                                                        medmod = 1.3
                                                                        longmod = 0
                                                                        await channel.send("{}'s class has been set to battlecruiser.".format(shipname))
                                                                    if classchoice == "7": 
                                                                        shipclass = 'Battleship'
                                                                        maxpoints = 3760
                                                                        healthmod = 1.15
                                                                        speedmod = (((- (1/3760) * math.log(3760) + 2000 * (5 / 3760)) - 100) / 100) + 1
                                                                        defencemod = 1.5
                                                                        closemod = 1.2
                                                                        medmod = 1.4
                                                                        longmod = 0.9
                                                                        await channel.send("{}'s class has been set to battleship.".format(shipname))
                                                                    if classchoice == "8": 
                                                                        shipclass = 'Lightcarrier'
                                                                        maxpoints = 9380
                                                                        healthmod = 1.2
                                                                        speedmod = (((- (1/9380) * math.log(9380) + 2000 * (5 / 9380)) - 100) / 100) + 1
                                                                        defencemod = 2
                                                                        closemod = 0.6
                                                                        medmod = 0.6
                                                                        longmod = 0.6
                                                                        await channel.send("{}'s class has been set to lightcarrier.".format(shipname))
                                                                    if classchoice == "9": 
                                                                        shipclass = 'Dreadnaught'
                                                                        maxpoints = 11250
                                                                        healthmod = 0.5
                                                                        speedmod = (((- (1/11250) * math.log(11250) + 2000 * (5 / 11250)) - 100) / 100) + 1
                                                                        defencemod = 1.7
                                                                        closemod = 1
                                                                        medmod = 1.3
                                                                        longmod = 1.3
                                                                        await channel.send("{}'s class has been set to dreadnaught.".format(shipname))
                                                                    if classchoice == "10": 
                                                                        shipclass = 'Carrier'
                                                                        maxpoints = 11880
                                                                        healthmod = 1.35
                                                                        speedmod = (((- (1/11880) * math.log(11880) + 2000 * (5 / 11880)) - 100) / 100) + 1
                                                                        defencemod = 2
                                                                        closemod = 0.6
                                                                        medmod = 0.6
                                                                        longmod = 0.6
                                                                        await channel.send("{}'s class has been set to carrier.".format(shipname))
                                                                    if classchoice == "11": 
                                                                        shipclass = 'Battlesphere'
                                                                        maxpoints = 175000
                                                                        healthmod = 1.4
                                                                        speedmod = (((- (1/175000) * math.log(175000) + 2000 * (5 / 175000)) - 100) / 100) + 1
                                                                        defencemod = 1.9
                                                                        closemod = 1.8
                                                                        medmod = 1.5
                                                                        longmod = 1
                                                                        await channel.send("{}'s class has been set to battlesphere.".format(shipname))
                                                                    if classchoice == "12":
                                                                        shipclass = 'Battleglobe'
                                                                        maxpoints = 9000000000
                                                                        healthmod = 1.5
                                                                        speedmod = (((- (1/9000000000) * math.log(9000000000) + 2000 * (5 / 9000000000)) - 100) / 100) + 1
                                                                        defencemod = 2
                                                                        closemod = 1
                                                                        medmod = 1.7
                                                                        longmod = 2
                                                                        await channel.send("{}'s class has been set to battleglobe.".format(shipname))
                                                                    spent = 0
                                                                    remain = int(maxpoints)
                                                                    await channel.send("You have {} points left.".format(remain))
                                                                    await channel.send("Please enter the amount of points you wish to spend on health")
                                                                    embedhealthallo = discord.Embed(title='Health', description='Points must not exceed remaining points.')
                                                                    embedhealthallo.add_field(name="Stats", value="""Remaining Points: {}
Max Points: {}
Health Points: -
Defense Points: -
Speed Points: -
Close Attack Points: -
Medium Attack Points: -
Long Attack Points: -""".format(remain, maxpoints), inline=False)
                                                                    try:
                                                                        await channel.send(embed=embedhealthallo)
                                                                        await client.wait_for('message', timeout=60)
                                                                    except asyncio.TimeoutError:
                                                                        await channel.send(embed=embedtimeout)
                                                                        canrun = False
                                                                    else:
                                                                        async for message in channel.history(limit=1):
                                                                            if message.author == user:
                                                                                health = int(message.content)
                                                                                if health > remain:
                                                                                    await channel.send("You do not have that many points.")
                                                                                else:
                                                                                    spent = health
                                                                                    remain = int(maxpoints) - spent
                                                                                    await channel.send("You have spent {} points on health. You have {} points left.".format(health, remain))
                                                                                    await channel.send("Please enter the amount of points you wish to spend on defense.")
                                                                                    embeddefenseallo = discord.Embed(title='Defense', description='Points must not exceed remaining points.')
                                                                                    embeddefenseallo.add_field(name="Stats", value="""Remaining Points: {}
Max Points: {}
Health Points: {}
Defense Points: -
Speed Points: -
Close Attack Points: -
Medium Attack Points: -
Long Attack Points: -""".format(remain, maxpoints, health), inline=False)
                                                                                    try:
                                                                                        await channel.send(embed=embeddefenseallo)
                                                                                        await client.wait_for('message', timeout=60)
                                                                                    except asyncio.TimeoutError:
                                                                                        await channel.send(embed=embedtimeout)
                                                                                        canrun = False
                                                                                    else:
                                                                                        async for message in channel.history(limit=1):
                                                                                            if message.author == user:
                                                                                                defense = int(message.content)
                                                                                                if defense > remain:
                                                                                                    await channel.send("You do not have that many ponts.")
                                                                                                else:
                                                                                                    spent = health + defense
                                                                                                    remain = int(maxpoints) - spent
                                                                                                    await channel.send("You have spent {} points on defense. You have {} points left.".format(defense, remain))
                                                                                                    await channel.send("Please enter the amount of points you wish to spend on speed.")
                                                                                                    embedspeedallo = discord.Embed(title='Speed', description='Points must not exceed remaining points.')
                                                                                                    embedspeedallo.add_field(name="Stats", value="""Remaining Points: {}
Max Points: {}
Health Points: {}
Defense Points: {}
Speed Points: -
Close Attack Points: -
Medium Attack Points: -
Long Attack Points: -""".format(remain, maxpoints, health, defense), inline=False)
                                                                                                    try:
                                                                                                        await channel.send(embed=embedspeedallo)
                                                                                                        await client.wait_for('message', timeout=60)
                                                                                                    except asyncio.TimeoutError:
                                                                                                        await channel.send(embed=embedtimeout)
                                                                                                        canrun = False
                                                                                                    else:
                                                                                                        async for message in channel.history(limit=1):
                                                                                                            if message.author == user:
                                                                                                                speed = int(message.content)
                                                                                                                if speed > remain:
                                                                                                                    await channel.send("You do not have that many ponts.")
                                                                                                                else:
                                                                                                                    spent = health + defense + speed
                                                                                                                    remain = int(maxpoints) - spent
                                                                                                                    await channel.send("You have spent {} points on speed. You have {} points left.".format(speed, remain))
                                                                                                                    await channel.send("Please enter the amount of points you wish to spend on close attack.")
                                                                                                                    embedcloseallo = discord.Embed(title='Close Attack', description='Points must not exceed remaining points.')
                                                                                                                    embedcloseallo.add_field(name="Stats", value="""Remaining Points: {}
Max Points: {}
Health Points: {}
Defense Points: {}
Speed Points: {}
Close Attack Points: -
Medium Attack Points: -
Long Attack Points: -""".format(remain, maxpoints, health, defense, speed), inline=False)
                                                                                                                    try:
                                                                                                                        await channel.send(embed=embedcloseallo)
                                                                                                                        await client.wait_for('message', timeout=60)
                                                                                                                    except asyncio.TimeoutError:
                                                                                                                        await channel.send(embed=embedtimeout)
                                                                                                                        canrun = False
                                                                                                                    else:
                                                                                                                        async for message in channel.history(limit=1):
                                                                                                                            if message.author == user:
                                                                                                                                closeatt = int(message.content)
                                                                                                                                if closeatt > remain:
                                                                                                                                    await channel.send("You do not have that many ponts.")
                                                                                                                                else:
                                                                                                                                    spent = health + defense + speed + closeatt
                                                                                                                                    remain = int(maxpoints) - spent
                                                                                                                                    await channel.send("You have spent {} points on close attack. You have {} points left.".format(closeatt, remain))
                                                                                                                                    await channel.send("Please enter the amount of points you wish to spend on medium attack.")
                                                                                                                                    embedmediumallo = discord.Embed(title='Medium Attack', description='Points must not exceed remaining points.')
                                                                                                                                    embedmediumallo.add_field(name="Stats", value="""Remaining Points: {}
Max Points: {}
Health Points: {}
Defense Points: {}
Speed Points: {}
Close Attack Points: {}
Medium Attack Points: -
Long Attack Points: -""".format(remain, maxpoints, health, defense, speed, closeatt), inline=False)
                                                                                                                                    try:
                                                                                                                                        await channel.send(embed=embedmediumallo)
                                                                                                                                        await client.wait_for('message', timeout=60)
                                                                                                                                    except asyncio.TimeoutError:
                                                                                                                                        await channel.send(embed=embedtimeout)
                                                                                                                                        canrun = False
                                                                                                                                    else:
                                                                                                                                        async for message in channel.history(limit=1):
                                                                                                                                            if message.author == user:
                                                                                                                                                medatt = int(message.content)
                                                                                                                                                if medatt > remain:
                                                                                                                                                    await channel.send("You do not have that many ponts.")
                                                                                                                                                else:
                                                                                                                                                    spent = health + defense + speed + closeatt + medatt
                                                                                                                                                    remain = int(maxpoints) - spent
                                                                                                                                                    await channel.send("You have spent {} points on medium attack. You have {} points left.".format(medatt, remain))
                                                                                                                                                    await channel.send("Please enter the amount of points you wish to spend on long attack.")
                                                                                                                                                    embedlongallo = discord.Embed(title='Medium Attack', description='Points must not exceed remaining points.')
                                                                                                                                                    embedlongallo.add_field(name="Stats", value="""Remaining Points: {}
Max Points: {}
Health Points: {}
Defense Points: {}
Speed Points: {}
Close Attack Points: {}
Medium Attack Points: {}
Long Attack Points: -""".format(remain, maxpoints, health, defense, speed, closeatt, medatt), inline=False)
                                                                                                                                                    try:
                                                                                                                                                        await channel.send(embed=embedlongallo)
                                                                                                                                                        await client.wait_for('message', timeout=60)
                                                                                                                                                    except asyncio.TimeoutError:
                                                                                                                                                        await channel.send(embed=embedtimeout)
                                                                                                                                                        canrun = False
                                                                                                                                                    else:
                                                                                                                                                        async for message in channel.history(limit=1):
                                                                                                                                                            if message.author == user:
                                                                                                                                                                longatt = int(message.content)
                                                                                                                                                                if longatt > remain:
                                                                                                                                                                    await channel.send("You do not have that many ponts.")
                                                                                                                                                                else:
                                                                                                                                                                    spent = health + defense + speed + closeatt + medatt + longatt
                                                                                                                                                                    remain = int(maxpoints) - spent
                                                                                                                                                                    await channel.send("You have spent {} points on long attack.".format(longatt))
                                                                                                                                                                    nation["ships"][shipname] = {}
                                                                                                                                                                    nation["ships"][shipname]["health"] = (health+1)*healthmod
                                                                                                                                                                    nation["ships"][shipname]["defense"] = (defense+1)*defencemod
                                                                                                                                                                    nation["ships"][shipname]["speed"] = (speed+1)*speedmod
                                                                                                                                                                    nation["ships"][shipname]["close"] = (closeatt+1)*closemod
                                                                                                                                                                    nation["ships"][shipname]["med"] = (medatt+1)*medmod
                                                                                                                                                                    nation["ships"][shipname]["long"] = (longatt+1)*longmod
                                                                                                                                                                    nation["ships"][shipname]["healthp"] = health
                                                                                                                                                                    nation["ships"][shipname]["defensep"] = defense
                                                                                                                                                                    nation["ships"][shipname]["speedp"] = speed
                                                                                                                                                                    nation["ships"][shipname]["closep"] = closeatt
                                                                                                                                                                    nation["ships"][shipname]["medp"] = medatt
                                                                                                                                                                    nation["ships"][shipname]["longp"] = longatt                                                                                                                                                      
                                                                                                                                                                    with open(nationfile, "w") as outfile:
                                                                                                                                                                        json.dump(nation, outfile)
                                                                                                                                                                    await channel.send("Ship successfuly created.")
                                                                                                                                                                    embedsummary = discord.Embed(title='Summary', description=shipname)
                                                                                                                                                                    embedsummary.add_field(name='Properties', value="""Nation: {}
Class: {}
Name: {}""".format(nationname, shipclass, shipname), inline=False)
                                                                                                                                                                    healthscore = nation["ships"][shipname]['health']
                                                                                                                                                                    defensescore = nation["ships"][shipname]['defense']
                                                                                                                                                                    speedscore = nation["ships"][shipname]['speed']
                                                                                                                                                                    closescore = nation["ships"][shipname]['close']
                                                                                                                                                                    medscore = nation["ships"][shipname]['med']
                                                                                                                                                                    longscore = nation["ships"][shipname]['long']
                                                                                                                                                                    embedsummary.add_field(name='Stats', value="""Health: {}
Defense: {}
Speed: {}
Close Attack: {}
Medium Attack: {}
Long Attack: {}""".format(healthscore, defensescore, speedscore, closescore, medscore, longscore), inline=False)
                                                                                                                                                                    await channel.send(embed=embedsummary)
                                                                                                                                                                    canrun = False
                                else:
                                    await channel.send("You do not own that nation.")
                if message.content == "fleet" and message.author == user:
                    try:
                        await channel.send("Please enter the name of the nation that you want to create the fleet in.")
                        await client.wait_for('message', timeout=60)
                    except asyncio.TimeoutError:
                        await channel.send(embed=embedtimeout)
                        canrun = False
                    else:
                        async for message in channel.history(limit=1):
                            nationname = message.content
                            nationfile = message.content + ".txt"
                            # if nation exists: true, proceed
                            try:
                                f = open(nationfile)
                                f.close()
                            except FileNotFoundError:
                                await channel.send("That nation does not exist.")
                                canrun = False
                            else:
                                with open(nationfile) as json_file:
                                    nation = json.load(json_file)
                                if nation["userid"] == userid:
                                    try:
                                        await channel.send("Please enter the name of the fleet.")
                                        await client.wait_for('message', timeout=60)
                                    except asyncio.TimeoutError:
                                        await channel.send(embed=embedtimeout)
                                        canrun = False
                                    else:
                                        async for message in channel.history(limit=1):
                                            if message.author == user:
                                                fleetname = message.content
                                                # if fleet exists, false: proceed
                                                if keys_exists(nation, "fleets", fleetname):
                                                    await channel.send("You have already created a fleet with that name.")
                                                    canrun = False
                                                else:
                                                    nation["fleets"][fleetname] = {}
                                                    fleetcanrun = True
                                                    while fleetcanrun == True and canrun == True:
                                                        try:
                                                            await channel.send("What ship would you like to add to {}?".format(fleetname))
                                                            await client.wait_for('message', timeout=60)
                                                        except asyncio.TimeoutError:
                                                            await channel.send(embed=embedtimeout)
                                                            canrun = False
                                                        else:
                                                            async for message in channel.history(limit=1):
                                                                if message.author == user:
                                                                    shipadd = message.content
                                                                    if shipadd == "cancel":
                                                                        await channel.send("Process cancelled.")
                                                                        canrun =  False
                                                                    else:
                                                                        if keys_exists(nation, "ships", shipadd):
                                                                            if keys_exists(nation, "fleets", fleetname, shipadd):
                                                                                await channel.send("You have already added {} to {}.".format(shipadd, fleetname))
                                                                                canrun = False
                                                                            else:
                                                                                try:
                                                                                    await channel.send("How many {} would you like to add to {}?".format(shipadd, fleetname))
                                                                                    await client.wait_for('message', timeout=60)
                                                                                except asyncio.TimeoutError:
                                                                                    await channel.send(embed=embedtimeout)
                                                                                    canrun = False
                                                                                else:
                                                                                    async for message in channel.history(limit=1):
                                                                                        if message.author == user:
                                                                                            try:
                                                                                                shipamount = int(message.content)
                                                                                            except ValueError:
                                                                                                await channel.send(embed=embedvalueerror)
                                                                                            else:
                                                                                                # if ship already in dic; false: proceed
                                                                                                if shipamount <= 0:
                                                                                                    await channel.send("Please enter an integer greater than 0.")
                                                                                                    canrun = False
                                                                                                else:
                                                                                                    if keys_exists(nation, "fleets", fleetname, shipadd):
                                                                                                        await channel.send("You have already added {} to {}".format(shipadd, fleetname))
                                                                                                        canrun = False
                                                                                                    else:
                                                                                                        nation["fleets"][fleetname][shipadd] = shipamount
                                                                                                        with open(nationfile, "w") as outfile:
                                                                                                            json.dump(nation, outfile)
                                                                                                        await channel.send("Fleet updated. Would you like to add another ship to {}? (yes/no)".format(fleetname))
                                                                                                        try:
                                                                                                            await client.wait_for('message', timeout=60)
                                                                                                        except asyncio.TimeoutError:
                                                                                                            await channel.send(embed=embedtimeout)
                                                                                                            canrun = False
                                                                                                        else:
                                                                                                            async for message in channel.history(limit=1):
                                                                                                                if message.author == user:
                                                                                                                    if message.content == "yes":
                                                                                                                        fleetcanrun = True
                                                                                                                    if message.content == "no":
                                                                                                                        fleetdic = nation["fleets"][fleetname]
                                                                                                                        amountlist = [*fleetdic.values()]
                                                                                                                        shipnamelist = [*fleetdic.keys()]
                                                                                                                        embedfleetsummary = discord.Embed(title=fleetname)
                                                                                                                        for i in range(0, len(amountlist)):
                                                                                                                            embedfleetsummary.add_field(name=shipnamelist[i], value = "{} ships".format(amountlist[i]), inline = True)
                                                                                                                        await channel.send(embed=embedfleetsummary)
                                                                                                                        canrun = False
                                                                        else:
                                                                            await channel.send("That ship does not exist.")
                                                                            canrun = False
                                else:
                                    await channel.send("You do not own that nation.")
                                    canrun = False
                else:
                    if message.author == user:
                        canrun = False
    if canrun == False:
        if channel == client.get_channel(764017189279236096):
            channel1available = True
            role4 = 'tufbot 1' #role to add
            await user.remove_roles(discord.utils.get(user.guild.roles, name=role4))
        elif channel == client.get_channel(764017265125228544):
            channel2available = True
            role5 = 'tufbot 2' #role to add
            await user.remove_roles(discord.utils.get(user.guild.roles, name=role5))
        elif channel == client.get_channel(764017300424622100):
            channel3available = True
            role6 = 'tufbot 3' #role to add
            await user.remove_roles(discord.utils.get(user.guild.roles, name=role6))

@client.command(name='edit')
async def edit(ctx):
    return

@client.command(name='delete')
async def delete(ctx):
    global channel1available
    global channel2available
    global channel3available
    user = ctx.message.author
    userid = ctx.author.id
    canrun = None
    if channel1available == True:
        channel1available = False
        channel = client.get_channel(764017189279236096)
        role1 = 'tufbot 1' #role to add
        await user.add_roles(discord.utils.get(user.guild.roles, name=role1))
        canrun = True
    elif channel2available == True:
        channel2available = False
        channel = client.get_channel(764017265125228544)
        role2 = 'tufbot 2' #role to add
        await user.add_roles(discord.utils.get(user.guild.roles, name=role2))
        canrun = True
    elif channel3available == True:
        channel3available = False
        channel = client.get_channel(764017300424622100)
        role3 = 'tufbot 3' #role to add
        await user.add_roles(discord.utils.get(user.guild.roles, name=role3))
        canrun = True
    else:
        await ctx.send("All channels are currently unavailable. Please try again later.")
    while canrun == True:
        await channel.send("<@{}>, please move here.".format(userid))
        await channel.send("What would you like to delete? (nation/ship/fleet)")
        try:
            await client.wait_for('message', timeout=60)
        except asyncio.TimeoutError:
            await channel.send(embed=embedtimeout)
            canrun = False
        else:
            async for message in channel.history(limit=1):
                if message.content == "nation" and message.author == user:
                    await channel.send("What is the name of the nation?")
                    try:
                        await client.wait_for('message', timeout=60)
                    except asyncio.TimeoutError:
                        await channel.send(embed=embedtimeout)
                        canrun = False
                    else:
                        async for message in channel.history(limit=1):
                            if message.author == user:
                                filename = message.content + ".txt"
                                nationname = message.content
                                try:
                                    f = open(filename)
                                    f.close()
                                except FileNotFoundError:
                                    await channel.send("That nation does not exist.")
                                    canrun = False
                                else:
                                    with open(filename) as json_file:
                                        nationfile = json.load(json_file)
                                    if nationfile["userid"] == userid:
                                        os.remove(filename)
                                        await channel.send("{} removed.".format(nationname))
                                        canrun = False
                                    else:
                                        await channel.send("You do not own this nation!")
                                        canrun = False
                if message.content == "ship" and message.author == user:
                    await channel.send("What is the name of the nation that contains the ship you wish to remove?")
                    try:
                        await client.wait_for('message', timeout=60)
                    except asyncio.TimeoutError:
                        await channel.send(embed=embedtimeout)
                        canrun = False
                    else:
                        async for message in channel.history(limit=1):
                            if message.author == user:
                                filename = message.content + ".txt"
                                nationname = message.content
                                try:
                                    f = open(filename)
                                    f.close()
                                except FileNotFoundError:
                                    await channel.send("That nation does not exist.")
                                    canrun = False
                                else:
                                    await channel.send("What is that name of the ship you wish to remove?")
                                    try:
                                        await client.wait_for('message', timeout=60)
                                    except asyncio.TimeoutError:
                                        await channel.send(embed=embedtimeout)
                                        canrun = False
                                    else:
                                        async for message in channel.history(limit=1):
                                            if message.author == user:
                                                shipname = message.content
                                                with open(filename) as json_file:
                                                    nation = json.load(json_file)
                                                if nation["userid"] == userid:
                                                    if keys_exists(nation, "ships", shipname):
                                                        del nation["ships"][shipname]
                                                        with open(filename, 'w') as outfile:
                                                            json.dump(nation, outfile)
                                                        await channel.send("{} has been deleted.".format(shipname))
                                                        canrun = False
                                                    else:
                                                        await channel.send("{} does not exist.".format(shipname))
                                                        canrun = False
                                                else:
                                                    await channel.send("You do not own this nation!")
                                                    canrun = False
                if message.content == "fleet" and message.author == user:
                    await channel.send("What is the name of the nation that contains the fleet you wish to remove?")
                    try:
                        await client.wait_for('message', timeout=60)
                    except asyncio.TimeoutError:
                        await channel.send(embed=embedtimeout)
                        canrun = False
                    else:
                        async for message in channel.history(limit=1):
                            if message.author == user:
                                filename = message.content + ".txt"
                                nationname = message.content
                                try:
                                    f = open(filename)
                                    f.close()
                                except FileNotFoundError:
                                    await channel.send("That nation does not exist.")
                                    canrun = False
                                else:
                                    await channel.send("What is that name of the fleet you wish to remove?")
                                    try:
                                        await client.wait_for('message', timeout=60)
                                    except asyncio.TimeoutError:
                                        await channel.send(embed=embedtimeout)
                                        canrun = False
                                    else:
                                        async for message in channel.history(limit=1):
                                            if message.author == user:
                                                fleetname = message.content
                                                with open(filename) as json_file:
                                                    nation = json.load(json_file)
                                                if nation["userid"] == userid:
                                                    if keys_exists(nation, "fleets", shipname):
                                                        del nation["fleets"][shipname]
                                                        with open(filename, 'w') as outfile:
                                                            json.dump(nation, outfile)
                                                        await channel.send("{} has been deleted.".format(fleetname))
                                                        canrun = False
                                                    else:
                                                        await channel.send("{} does not exist.".format(fleetname))
                                                        canrun = False
                                                else:
                                                    await channel.send("You do not own this nation!")
                                                    canrun = False
    if canrun == False:
        if channel == client.get_channel(764017189279236096):
            channel1available = True
            role4 = 'tufbot 1' #role to add
            await user.remove_roles(discord.utils.get(user.guild.roles, name=role4))
        elif channel == client.get_channel(764017265125228544):
            channel2available = True
            role5 = 'tufbot 2' #role to add
            await user.remove_roles(discord.utils.get(user.guild.roles, name=role5))
        elif channel == client.get_channel(764017300424622100):
            channel3available = True
            role6 = 'tufbot 3' #role to add
            await user.remove_roles(discord.utils.get(user.guild.roles, name=role6))

@client.command(name='view')
async def view(ctx):
    global channel1available
    global channel2available
    global channel3available
    user = ctx.message.author
    userid = ctx.author.id
    canrun = None
    if channel1available == True:
        channel1available = False
        channel = client.get_channel(764017189279236096)
        role1 = 'tufbot 1' #role to add
        await user.add_roles(discord.utils.get(user.guild.roles, name=role1))
        canrun = True
    elif channel2available == True:
        channel2available = False
        channel = client.get_channel(764017265125228544)
        role2 = 'tufbot 2' #role to add
        await user.add_roles(discord.utils.get(user.guild.roles, name=role2))
        canrun = True
    elif channel3available == True:
        channel3available = False
        channel = client.get_channel(764017300424622100)
        role3 = 'tufbot 3' #role to add
        await user.add_roles(discord.utils.get(user.guild.roles, name=role3))
        canrun = True
    else:
        await ctx.send("All channels are currently unavailable. Please try again later.")
    while canrun == True:
        await channel.send("What would you like to view? (ship/fleet)")
        try:
            await client.wait_for("message", timeout=60)
        except asyncio.TimeoutError:
            await channel.send(embed=embedtimeout)
            canrun = False
        else:
            async for message in channel.history(limit=1):
                if message.author == user:
                    if message.content == "ship":
                        await channel.send("Which nation contains the ship you wish to view?")
                        try:
                            await client.wait_for("message", timeout=60)
                        except asyncio.TimeoutError:
                            await channel.send(embed=embedtimeout)
                            canrun = False
                        else:
                            async for message in channel.history(limit=1):
                                if message.author == user:
                                    nation = message.content
                                    nationfile = nation + ".txt"
                                    try:
                                        with open(nationfile) as infile:
                                            nationjsonfile = json.load(infile)
                                    except IOError:
                                        await channel.send("That nation does not exist.")
                                        canrun = False
                                    else:
                                        await channel.send("What is the name of the ship you wish to view?")
                                        try:
                                            await client.wait_for("message", timeout=60)
                                        except asyncio.TimeoutError:
                                            await channel.send(embed=embedtimeout)
                                        else:
                                            async for message in channel.history(limit=1):
                                                if message.author == user:
                                                    shipname = message.content
                                                    if keys_exists(nationjsonfile, "ships", shipname):
                                                        healthscore = nationjsonfile["ships"][shipname]['health']
                                                        defensescore = nationjsonfile["ships"][shipname]['defense']
                                                        speedscore = nationjsonfile["ships"][shipname]['speed']
                                                        closescore = nationjsonfile["ships"][shipname]['close']
                                                        medscore = nationjsonfile["ships"][shipname]['med']
                                                        longscore = nationjsonfile["ships"][shipname]['long']
                                                        embedshipview = discord.Embed(title=shipname, description="{} (<@{}>)".format(nation, userid))
                                                        embedshipview.add_field(name='Stats', value="""Health: {}
Defense: {}
Speed: {}
Close Attack: {}
Medium Attack: {}
Long Attack: {}""".format(healthscore, defensescore, speedscore, closescore, medscore, longscore))
                                                        await channel.send(embed=embedshipview)
                                                        canrun = False
                                                    else:
                                                        await channel.send("That ship does not exist.")
                                                        canrun = False
                    if message.content == "fleet":
                        await channel.send("Which nation contains the fleet you wish to view?")
                        try:
                            await client.wait_for("message", timeout=60)
                        except asyncio.TimeoutError:
                            await channel.send(embed=embedtimeout)
                            canrun = False
                        else:
                            async for message in channel.history(limit=1):
                                if message.author == user:
                                    nation = message.content
                                    nationfile = nation + ".txt"
                                    try:
                                        with open(nationfile) as infile:
                                            nationjsonfile = json.load(infile)
                                    except IOError:
                                        await channel.send("That nation does not exist.")
                                        canrun = False
                                    else:
                                        try:
                                            await channel.send("What is the name of the fleet you wish to view?")
                                            await client.wait_for("message", timeout=60)
                                        except asyncio.TimeoutError:
                                            await channel.send(embed=embedtimeout)
                                        else:
                                            async for message in channel.history(limit=1):
                                                if message.author == user:
                                                    fleetname = message.content
                                                    if keys_exists(nationjsonfile, "fleets", fleetname):
                                                        fleetdic = nationjsonfile["fleets"][fleetname]
                                                        amountlist = [*fleetdic.values()]
                                                        shipnamelist = [*fleetdic.keys()]
                                                        embedfleetsummary = discord.Embed(title=fleetname, description="{} (<@{}>)".format(nation, userid))
                                                        for i in range(0, len(amountlist)):
                                                            embedfleetsummary.add_field(name=shipnamelist[i], value = "{} ships".format(amountlist[i]), inline = True)
                                                        await channel.send(embed=embedfleetsummary)
                                                        canrun = False
                                                    else:
                                                        await channel.send("That fleet does not exist.")
                                                        canrun = False
                    else:
                        if message.author == user:
                            canrun = False
    if canrun == False:
        if channel == client.get_channel(764017189279236096):
            channel1available = True
            role4 = 'tufbot 1' #role to add
            await user.remove_roles(discord.utils.get(user.guild.roles, name=role4))
        elif channel == client.get_channel(764017265125228544):
            channel2available = True
            role5 = 'tufbot 2' #role to add
            await user.remove_roles(discord.utils.get(user.guild.roles, name=role5))
        elif channel == client.get_channel(764017300424622100):
            channel3available = True
            role6 = 'tufbot 3' #role to add
            await user.remove_roles(discord.utils.get(user.guild.roles, name=role6))

@client.command(name='ping')
async def ping(ctx):
    await ctx.channel.send("pong")

@client.command(name='ding')
async def ding(ctx):
    await ctx.channel.send("dong")

@client.command(name='thatcher')
async def thatcher(ctx):
    await ctx.channel.send("She's still dead.")

@client.command(name='meme')
async def meme(ctx):
    await ctx.channel.send("school")

@client.command(name='8ball')
async def ball(ctx):
    listofballresponses = ["It is certain",
"Without a doubt",
"You may rely on it",
"Yes definitely",
"It is decidedly so",
"As I see it, yes",
"Most likely",
"Yes",
"Outlook good",
"Signs point to yes",
"Reply hazy try again", 
"Better not tell you now", 
"Ask again later", 
"Cannot predict now", 
"Concentrate and ask again", 
"Don’t count on it", 
"Outlook not so good", 
"My sources say no", 
"Very doubtful", 
"My reply is no"]
    ballrandom = random.randint(0, 19)
    message = listofballresponses[ballrandom]
    await ctx.channel.send(message)
    
# NATIONSTATES ----
# HELP
embedhelpnhappen = discord.Embed(title='National Happenings')
embedhelpnhappen.add_field(name='Argument', value="""!national_happenings <nation_name>

**nation_name** - name of the nation to get events from.""")

# GLOBAL VARS
now = datetime.now()
date_today = now.strftime("%d/%m/%Y")

# CONSTANTS
custom_time = 0.4
headers = {"User-Agent":'NATION_NAME'}
censusiddict = {"0" : "Civil rights", 
"1" : "Economy", 
"2" : "Political freedoms", 
"3" : "Population", 
"4" : "Wealth gaps", 
"5" : "Death rate", 
"6" : "Compassion", 
"7" : "Eco-friendliness", 
"8" : "Social conservatism", 
"9" : "Nudity", 
"10" : "Industry: Automobile manufacturing", 
"11" : "Industry: cheese exports", 
"12" : "Industry: basket weaving", 
"13" : "Industry: information technology", 
"14" : "Industry: pizza delivery", 
"15" : "Industry: trout fishing", 
"16" : "Industry: arms manufacturing", 
"17" : "Sector: agriculture", 
"18" : "Industry: beverage sales", 
"19" : "Industry: timber woodchipping", 
"20" : "Industry: mining", 
"21" : "Industry: insurance", 
"22" : "Industry: furniture restoration", 
"23" : "Industry: retail", 
"24" : "Industry: book publishing", 
"25" : "Industry: gambling", 
"26" : "Sector: manufacturing", 
"27" : "Government size", 
"28" : "Welfare", 
"29" : "Public healthcare", 
"30" : "Law enforcement", 
"31" : "Business subsidization", 
"32" : "Religiousness", 
"33" : "Income equality", 
"34" : "Niceness", 
"35" : "Rudeness", 
"36" : "Intelligence", 
"37" : "Ignorance", 
"38" : "Political apathy", 
"39" : "Health", 
"40" : "Cheerfulness", 
"41" : "Weather", 
"42" : "Compliance", 
"43" : "Safety", 
"44" : "Lifespan", 
"45" : "Ideological radicality", 
"46" : "Defense forces", 
"47" : "Pacifism", 
"48" : "Economic freedom", 
"49" : "Taxation", 
"50" : "Freedom from taxation", 
"51" : "Corruption", 
"52" : "Integrity", 
"53" : "Authoritarianism", 
"54" : "Youth rebelliousness", 
"55" : "Culture", 
"56" : "Employment", 
"57" : "Public transport", 
"58" : "Tourism", 
"59" : "Weaponization", 
"60" : "Recreational drug use", 
"61" : "obesity", 
"62" : "Secularism", 
"63" : "Environmental beauty", 
"64" : "Charmlessness", 
"65" : "Influence", 
"66" : "World assembly endorsements", 
"67" : "Averageness", 
"68" : "Human development index", 
"69" : "Primitiveness", 
"70" : "Scientific advancement", 
"71" : "Inclusiveness", 
"72" : "Average income", 
"73" : "Average income of poor", 
"74" : "Average income of rich", 
"75" : "Public education", 
"76" : "Economic output", 
"77" : "Crime", 
"78" : "Foreign aid", 
"79" : "Black market", 
"80" : "Residency", 
"81" : "Survivors", 
"82" : "zombies", 
"83" : "Dead", 
"84" : "Percentage zombies", 
"85" : "Average disposable income", 
"86" : "International artwork"}

# EXCEPTIONS
@client.event
async def on_command_error(ctx, error):
    if isinstance(error, discord.ext.commands.errors.MissingRequiredArgument):
        await ctx.send("A required argument is missing!")


# NATION
@client.command(name='noverview')
async def noverview(ctx, nationinput):
    try:
        async with ctx.typing():
            nation = str(nationinput)
            response = requests.get(f"https://www.nationstates.net/cgi-bin/api.cgi?nation={nation}", headers=headers)
            root = ElementTree.fromstring(response.content)
            nation = root.find("NAME").text
            nationurl = f"https://www.nationstates.net/nation={nation}"
            embednoverview = discord.Embed(title=nation, description="Overview", url=nationurl)
            flagurl = root.find("FLAG").text
            ntype = root.find("TYPE").text
            motto = root.find("MOTTO").text
            category = root.find("CATEGORY").text
            wastatus = root.find("UNSTATUS").text
            influence = root.find("INFLUENCE").text
            population_base = root.find("POPULATION").text
            population = population_base + " million"
            animal = root.find("ANIMAL").text
            region = root.find("REGION").text
            region_base = region.replace(" ", "_")
            region_link = f"https://www.nationstates.net/region={region_base}"
            currency = root.find("CURRENCY").text
            leader = root.find("LEADER").text
            capital = root.find("CAPITAL").text
            religion = root.find("RELIGION").text
            response2 = requests.get(f'https://www.nationstates.net/cgi-bin/api.cgi?nation={nation};q=census;mode=score;scale=66', headers=headers)
            root2 = ElementTree.fromstring(response2.content)
            endolen = root2[0][0][0]
            embednoverview.set_thumbnail(url=flagurl)
            embednoverview.add_field(name="National Information", value=f"""Name: The {ntype} of **{nation}**
Motto: *{motto}*
Classification: {category}
Population: {population}
Capital: {capital}
Leader: {leader}
Religion: {religion}
Currency: {currency}
Animal: {animal}""")
            embednoverview.add_field(name='International Information', value=f"""Region: [{region}]({region_link})
WA Status: {wastatus}
Endorsement Count: {endolen}
Influence: {influence}""", inline=False)
            await ctx.send(embed=embednoverview)
    except:
        await ctx.send("Nation cannot be found.")

@client.command(name='nhappenings')
async def nhappen(ctx, nationinput):
    try:
        async with ctx.typing():
            nation = str(nationinput)
            response = requests.get(f"https://www.nationstates.net/cgi-bin/api.cgi?nation={nation}&q=happenings", headers = headers)
            root = ElementTree.fromstring(response.content)
            response2 = requests.get(f"https://www.nationstates.net/cgi-bin/api.cgi?nation={nation}", headers=headers)
            root2 = ElementTree.fromstring(response2.content)
            flagurl = root2.find("FLAG").text
            nation = root2.find("NAME").text
            embednhappen = discord.Embed(title=nation, description="Happenings")
            embednhappen.set_thumbnail(url=flagurl)
            for happening in root.findall("HAPPENINGS"):
                for event in happening.findall("EVENT"):
                    text = event.find("TEXT").text.replace("@@", "**")
                    text = text.replace(nationinput, nation)
                    utc = int(event.find("TIMESTAMP").text)
                    utctime = str(datetime.utcfromtimestamp(utc).strftime('%d/%m/%Y %H:%M:%S'))
                    if date_today not in utctime:
                        pass
                    else:
                        if "Following new legislation" in text:
                            text.replace(f"Following new legislation in **{nation}**, ", "")
                            text.capitalize()
                            embednhappen.add_field(name="New Legislation", value=utctime + "\n" + text, inline=False)
                        elif "was ranked in the" in text:
                            embednhappen.add_field(name='New Badge', value=utctime + "\n" + text, inline=False)
                        elif "published" in text:
                            embednhappen.add_field(name='New Dispatch', value=utctime + "\n" + text, inline=False)
                        time.sleep(custom_time)

        await ctx.send(embed=embednhappen)
    except:
        await ctx.send("Nation cannot be found.")

@client.command(name='ncensus')
async def ncensus(ctx, nation, censusid, mode):
    try:
        async with ctx.typing():
            censusidinput = str(censusid)
            modeinput = str(mode)
            nationinput = str(nation)
            response = requests.get(f"https://www.nationstates.net/cgi-bin/api.cgi?nation={nationinput}&q=census&scale={censusidinput}&mode={modeinput}", headers = headers)
            root = ElementTree.fromstring(response.content)
            try:
                censusid = root[0].get("id")
            except:
                await ctx.send("Params are invalid.")
            else:
                result = root[0][0][0].text
                censusname = censusiddict[censusidinput]
                embedncensus = discord.Embed(title=censusname, description=result)
                embedncensus.add_field(name="Details", value=f"""Census ID: {censusidinput}
Mode: {mode}""")
                await ctx.send(embed=embedncensus)
    except:
        await ctx.send("Nation cannot be found.")
    
client.run("BOT_TOKEN")
