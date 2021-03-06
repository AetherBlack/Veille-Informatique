#!/usr/bin/python3

from discord.ext import commands, tasks

import sys

from const import TOKEN

# Prefix du bot
bot = commands.Bot(command_prefix='!')

# Au lancement
@bot.event
async def on_ready():
    print("Logged in as {0}\n{1}".format(bot.user.name, bot.user.id))
    print("------------------")
    # Recuperation de l'id des channels
    global channel
    channel = list()
    for guild in bot.guilds:
        #print(guild.channels)
        channel.append(guild.channels)
    await bot.close()

if __name__ == "__main__":
    bot.run(TOKEN)
    
    for index, guild in enumerate(channel):
        print("[+] Guild {0}".format(index))
        for value in guild:
            print("\t", value.name, value.id)