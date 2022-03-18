#!/usr/bin/python3

from discord.ext import commands

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
        # Log Guild index
        print("[+] Guild {0}".format(index))

        # For channel in guild
        for chann in guild:
            # Check if the channel is a category
            if chann.category is None:
                print(f"\t{chann.name} - {chann.id}")

                # For each channel in guild
                for value in guild:
                    # Check if the channel is a subchannel of the category for the guild
                    if str(value.category) == str(chann.name):
                        print(f"\t\t{value.name} - {value.id}")
            else:
                continue
