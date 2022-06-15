#!/usr/bin/python3

from discord.ext import commands

import discord
import sys
import os

from const import TOKEN, JSON_RSS
from fts.fluxrss import FluxRSS


# Bot prefix
bot = commands.Bot(command_prefix='!')

# When the bot is ready after launch
@bot.event
async def on_ready():
    print("Logged in as {0}\n{1}".format(bot.user.name, bot.user.id))
    print('--------------------------------')

    # Change the presence of the bot
    await bot.change_presence(status=discord.Status.online, activity=discord.Game("Flux RSS"))
    
    # Delete help command
    bot.remove_command("help")

    # Get the real Current Working Directory
    CWD = os.path.dirname(os.path.realpath(__file__))

    # Get the rss instance
    fluxrss = FluxRSS(bot, CWD)

    # Launch main rss
    bot.loop.create_task(fluxrss.feedrss(JSON_RSS))


if __name__ == "__main__":
    # Add Current Working Directory on the path
    sys.path.append(os.getcwd())

    # Launch the bot
    bot.run(TOKEN)
