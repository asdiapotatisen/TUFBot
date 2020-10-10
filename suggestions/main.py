import os
import discord
import math
import asyncio
from discord.ext import commands
client = commands.Bot(command_prefix='!', help_command=None)

embedtimeout = discord.Embed(title='Process Failed')
embedtimeout.add_field(name='Reason', value='Timeout', inline=False)

@client.command(name='suggest')
async def suggest(ctx):
    channel = client.get_channel(664615244236062727)
    user = ctx.message.author
    userid = ctx.author.id
    await channel.send("Please give a brief description of the problem.")
    try:
        await client.wait_for('message', timeout=60)
    except asyncio.TimeoutError:
        await channel.send(embed=embedtimeout)
    else:
        async for message in channel.history(limit=1):
            if message.author == user:
                problem = message.content
                await channel.send("Please provide details regarding the problem.")
                try:
                    await client.wait_for('message', timeout=60)
                except asyncio.TimeoutError:
                    await channel.send(embed=embedtimeout)
                else:
                    async for message in channel.history(limit=1):
                        if message.author == user:
                            details = message.content
                            await channel.send("Please propose a solution.")
                            try:
                                await client.wait_for('message', timeout=60)
                            except asyncio.TimeoutError:
                                await channel.send(embed=embedtimeout)
                            else:
                                async for message in channel.history(limit=1):
                                    if message.author == user:
                                        solution = message.content
                                        await channel.send("Process complete.")
                                        embedsuggest = discord.Embed(title='Suggestion', description="Author: <@{}>".format(userid))
                                        embedsuggest.add_field(name="Problem", value="{}".format(problem), inline=False)
                                        embedsuggest.add_field(name="Details", value="{}".format(details), inline=False)
                                        embedsuggest.add_field(name="Solution", value="{}".format(solution), inline=False)
                                        channel = client.get_channel(666213834675060749)
                                        await channel.send(embed=embedsuggest)
client.run("BOT TOKEN")
