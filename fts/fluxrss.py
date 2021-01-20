#!/usr/bin/python3

from urllib.parse import urlparse

import feedparser
import requests
import asyncio
import discord
import hashlib
import os

from const import CHANNEL_RSS, WAIT_UNTIL_NEW_CHECK, \
    SQLITE_FOLDER_NAME, SQLITE_FILE_NAME
from fts.database import Database

class FluxRSS:

    """
    Class of FluxRSS.
    Get news of the feedrss url parse in args.
    """

    def __init__(self, bot, cwd):
        """
        Initialize class
        @param => DiscordBot: `bot`: Discord Bot Instance.
        @param => str: `cwd`: Current Working Directory of main.py file.
        """
        # Discord
        self.bot = bot
        self.bot_username = self.bot.user.name
        self.rss_channel = self.bot.get_channel(CHANNEL_RSS)
        # Path
        self.cwd = cwd
        # Database
        self.db_path = os.path.join(self.cwd, SQLITE_FOLDER_NAME)
        self.database = Database(self.db_path, SQLITE_FILE_NAME)


    def get_news(self, url):
        """
        Get the news of the rss feed.
        @param => str: `url`: url of the rss feed.
        Return dict with an int index key and
        title, description and link in a list for the value.
        """
        dict_news = dict()

        # Get the content of the requests
        content = requests.get(url).text

        # Parse the content
        parser = feedparser.parse(content)
        # Set the root
        parser = parser["entries"]

        # Get the number of news
        news_number = len(parser)

        # Construct the dict
        for index in range(news_number):
            # Get the title
            title = parser[index]["title"]
            # Get the description
            description = parser[index]["content"][0]["value"]
            # Get the link
            link = parser[index]["links"][0]["href"]

            # Set list
            args = [
                title, description, link
            ]

            # Add the list to the dict
            dict_news[str(index)] = args

        # Return the dict
        return dict_news


    def is_new(self, title, description, link):
        """
        Return True if the news in the feed is new.
        @param => str: `title`: Title of the news.
        @param => str: `description`: Description of the news.
        @param => str: `link`: Link of the rss feed.
        """
        # Hash description
        hash_description = hashlib.sha256(bytes(description, "utf-8", errors="ignore")).hexdigest()
        # Return the check of the query
        return self.database.isNewsExists(title, link, hash_description)


    def embeded_msg(self, name, title, content, link):
        """
        Create the embeded message and send it to discord.
        @param => str: `name`: Name set in const. Categorie of the news
        @param => str: `title`: Title of the news.
        @param => str: `content`: Content description of the news.
        @param => str: `link`: Link of the news.
        """
        # Set the Name, description and color on the left
        news = discord.Embed(title=name, description="News :", color=0x00ff00)

        #Set bot name and profil picture
        news.set_author(name=self.bot_username, icon_url=self.bot.user.avatar_url)

        #Set the description and the link for the main message
        content = content + "\n" + link
        news.add_field(name=title, value=content, inline=False)

        #Show the bot username in footer
        news.set_footer(text="Generate by @{0}".format(self.bot_username))

        # Return the final Discord embeded message
        return news


    async def feedrss(self, json_rss):
        """
        Get the news and send it to the channel.
        @param => dict: `json_rss`: JSON data of the RSS Flux.
        """
        # Show const for the format
        self.json_rss = json_rss

        # While the connection is not closed
        while not self.bot.is_closed():

            # For each key
            for key, sections in self.json_rss.items():

                # Get the root name set in const
                root = key

                # For each sections
                for section in sections:

                    # Get the name of the section
                    name = section["name"]

                    # For each link in the section
                    for link in section["link"]:

                        # Get title, description and link in a dict
                        dict_news = self.get_news(link)

                        # Verify if the news already exists
                        for value in dict_news.values():
                            # Get title
                            title = value[0]
                            # Get description
                            description = value[1]
                            # Get link
                            link = value[2]

                            # Check if the news is new
                            if not self.is_new(title, description, link):
                                # Hash the description
                                hash_description = hashlib.sha256(bytes(description, "utf-8", errors="ignore")).hexdigest()
                                # write the news into the database
                                self.database.AddNews(root, name, title, hash_description, link)
                                #Create the discord message
                                message = self.embeded_msg(name, title, description, link)
                                #Send to discord
                                await self.rss_channel.send(embed=message)

            # Wait until the next verification
            await asyncio.sleep(WAIT_UNTIL_NEW_CHECK)
