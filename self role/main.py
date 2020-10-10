import os
import discord
import asyncio
from discord.ext import commands
client = commands.Bot(command_prefix='!', help_command=None)

embedrole = discord.Embed(title='Available roles')
embedrole.add_field(name='Do !role <add/remove> <rolename> to receive the role', value="""Dead, but hidden
map editor
#Anime
SHB
Nova Aeterna
norrpakten
GL
Eternal Cosmos""")

embedhelp = discord.Embed(title='Help Menu')
embedhelp.add_field(name='!roles', value="Lists out all roles avaialable.", inline=False)
embedhelp.add_field(name="!role <action> <name>", value ="""Adds/Removes a role.
**Parameters**
action: "add" or "remove"
name: Role's name. Must be on the list (!roles)""", inline=False)

@client.command(name='roles')
async def roles(ctx):
    await ctx.send(embed=embedrole)

@client.command(name='help')
async def help(ctx):
    await ctx.send(embed=embedhelp)

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
        await ctx.send("Invalid action.")
        
client.run("")
