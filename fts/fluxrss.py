#!/usr/bin/python3

import feedparser
import requests
import asyncio
import discord
import hashlib
import time
import os

from const import CHANNEL_RSS, WAIT_UNTIL_NEW_CHECK, \
    SQLITE_FOLDER_NAME, SQLITE_FILE_NAME
from fts.database import Database
from fts.cleandatabase import CleanDatabase
from fts.Utils import Filter
from fts.RSS import RSS


class FluxRSS:

    """
    Class of FluxRSS.
    Get news of the feedrss url parse in args.
    """

    def __init__(self, bot: discord.Client, cwd: str) -> str:
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

    def get_news(self, url: str) -> dict:
        """
        Get the news of the rss feed.
        @param => str: `url`: url of the rss feed.
        :returns dict with an int index key and
            title, description and link in a list for the value.
        """
        dict_news = dict()

        # Get the content of the requests
        content = requests.get(url, headers={"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:98.0) Gecko/20100101 Firefox/98.0"}).text

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
            description = parser[index]["description"]
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

    def is_new(self, root: str, name: str, title: str, description: str, link: str) -> bool:
        """
        @param => str: `root`: Root name of the news.
        @param => str: `title`: Title of the news.
        @param => str: `description`: Description of the news.
        @param => str: `link`: Link of the rss feed.
        :returns True if the news in the feed is new.
        """
        # Hash description
        hash_description = hashlib.sha256(bytes(description, "utf-8", errors="ignore")).hexdigest()
        # Return the check of the query
        return not self.database.isNewsExists(root, name, title, hash_description, link)

    def embeded_msg(self, root: str, name: str, title: str, content: str, link: str, color: discord.Colour) -> discord.Embed:
        """
        Create the embeded message and send it to discord.
        @param => str: `root`: Name of the Website.
        @param => str: `name`: Name set in const. Categorie of the news
        @param => str: `title`: Title of the news.
        @param => str: `content`: Content description of the news.
        @param => str: `link`: Link of the news.
        @param => discord.Colour: `color`: Color for the left panel.
        :returns a embeded discord messsage
        """
        # Set the Name, description and color on the left
        news = discord.Embed(title=f"{root} - {name}", description="News :", color=(color or 0x00ff00))

        #Set bot name and profil picture
        news.set_author(name=self.bot_username, icon_url=self.bot.user.avatar_url)

        #Set the description and the link for the main message
        content = content + "\n" + link
        news.add_field(name=title, value=content[:1024], inline=False)

        #Show the bot username in footer
        news.set_footer(text=f"Generate by @{self.bot_username}")

        # Return the final Discord embeded message
        return news

    def check_news(self, root: str, name: str, title: str, description: str, link: str, filter: dict) -> bool:
        """
        Check if the news is new and if they respect filter.
        @param => str: `root`: Name of the Website.
        @param => str: `name`: Name set in const. Categorie of the news
        @param => str: `title`: Title of the news.
        @param => str: `description`: Description of the news.
        @param => str: `link`: Link of the rss feed.
        @param => dict: `filter`: Custom filter of the news.
        :returns True if the news is good.
        """
        # Check if the news is new
        is_news_new = self.is_new(root, name, title, description, link)

        is_filter_good = True
        # Check if the news match filter
        if filter:
            is_filter_good = all([
                    Filter.checkTitle(filter, title),
                    Filter.checkDescription(filter, description),
                    Filter.checkLink(filter, link)
                    ])

        return all([is_news_new, is_filter_good])


    async def feedrss(self, json_rss: dict) -> None:
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

                # For each sections
                for index_section, section in enumerate(sections):

                    # Get class for RSS
                    rssSection = RSS(key, section)

                    # Log
                    print(f"[+] Get RSS feed for {key} - {rssSection.name} {time.strftime('%R:%S %F')}")

                    # Check if the cleaning database is already launched
                    if isinstance(rssSection.wait_time, str):

                        # Launch the function to clean the database
                        Thread = CleanDatabase(rssSection.root, rssSection.name, rssSection.wait_time, self.db_path, SQLITE_FILE_NAME)
                        Thread.start()

                        # Change the variable type of the clean line in json_rss to launch relaunch the requests
                        self.json_rss[rssSection.root][index_section]["clean"] = True

                    # For each link in the section
                    for link in rssSection.link:

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

                            # Check if the news is good
                            if self.check_news(rssSection.root, rssSection.name, title, description, link, rssSection.filter):
                                # Hash the description
                                hash_description = hashlib.sha256(bytes(description, "utf-8", errors="ignore")).hexdigest()
                                # write the news into the database
                                self.database.AddNews(rssSection.root, rssSection.name, title, hash_description, link)
                                # Create the discord message
                                message = self.embeded_msg(rssSection.root, rssSection.name, title[:256], description, link, rssSection.color)

                                # Send to discord
                                await self.rss_channel.send(embed=message)

            # Wait until the next verification
            await asyncio.sleep(WAIT_UNTIL_NEW_CHECK)
