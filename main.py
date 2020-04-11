#!/usr/bin/python3
# -*- coding: utf-8 -*-
from discord.ext import commands

import discord
import sys
import os

from const import TOKEN, FLUX_RSS
from fts.fluxrss import FluxRSS

# Prefix du bot.
bot = commands.Bot(command_prefix='!')


# Lancement des taches du bot.
@bot.event
async def on_ready():
    print("Logged in as {0}\n{1}".format(bot.user.name, bot.user.id))
    print('--------------------------------')
    # Change la présence du bot
    await bot.change_presence(status=discord.Status.online, activity=discord.Game("Flux RSS"))
    # Suppression et importation des commandes.
    bot.remove_command("help")
    # Lancement du fluxrss
    #  Recuperation du CWD
    CWD = os.getcwd()
    #fluxrss = FluxRSS(bot)
    for feedrss in FLUX_RSS:
        bot.loop.create_task(FluxRSS(bot).feedrss(CWD, feedrss))


if __name__ == "__main__":
    #Ajout du dossier courant dans la variable d'environnement
    sys.path += [os.getcwd()]
    #Lancement du bot
    bot.run(TOKEN)
