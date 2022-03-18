#!/usr/bin/python3

from discord.ext import commands

from const import TOKEN


# Bot prefix
bot = commands.Bot(command_prefix='!')

# When the bot is ready after launch
@bot.event
async def on_ready():
    print(f"Logged in as {bot.user.name}\n{bot.user.id}")
    print("------------------")

    # Get id of each channel
    global channel
    channel = list()

    # For each guild were the bot is in
    for guild in bot.guilds:
        channel.append(guild.channels)

    # Close the bot connection
    await bot.close()

if __name__ == "__main__":
    # Launch the bot
    bot.run(TOKEN)

    # For each guild
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
