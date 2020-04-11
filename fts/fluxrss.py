#!/usr/bin/python3

from urllib.parse import urlparse

import feedparser
import requests
import asyncio
import discord
import os

from const import CHANNEL_RSS, WAIT_NEW_NEWS

class FluxRSS:

    """
    Class of FluxRSS.
    Get news of the feedrss url parse in args.
    """

    def __init__(self, bot):
        """
        Set some var like:
        > self.bot = Class Bot
        > self.bot_username = Username of the bot
        > self.rss_channel = Instance for send message in the channel
        """
        self.bot = bot
        self.bot_username = self.bot.user.name
        self.rss_channel = self.bot.get_channel(CHANNEL_RSS)

    def mkdir(self, folder):
        """
        make directory for save the feedrss file
        > folder = folder of the feedrss
        """
        #Join the path to the folder
        self.feedrss_path = os.path.join(self.cwd, folder)

        #Verify if the folder exist and then create it
        if os.path.isdir(self.feedrss_path) is False: os.mkdir(self.feedrss_path)
    
    def number_of_news(self, content):
        """
        Return the number of news
        > content = Content of the feedrss
        """
        return feedparser.parse(content)['entries'].__len__()

    def get_news(self, news_content=None):
        """
        Get the news of the url feed.
        Return the title, content and link.
        """
        #Var returned title, description and link
        title_list = list()
        description_list = list()
        link_list = list()
        #Get the content of the requests
        if news_content is None:
            content = requests.get(self.url).text
        else:
            content = news_content
        #Parse the content
        parserss = feedparser.parse(content)
        #Get the number of news
        number_news = self.number_of_news(content)

        #Get all news
        for news in range(number_news):
            #Add title
            title = parserss['entries'][news]['title']
            title_list.append(title)
            #Add description
            description = parserss['entries'][news]['content'][0]['value']
            description_list.append(description)
            #Add link
            link = parserss['entries'][news]['links'][0]['href']
            link_list.append(link)

        #Return the content of the requests if news_content if None
        if news_content is None:
            return title_list, description_list, link_list, content
        else:
            return title_list, description_list, link_list

    def write(self, _file, mode, content):
        """
        Write into the _file in mode mode the content content.
        > _file = name file
        > mode = w for write or a for append
        > content = Content to write
        """
        #Write into _file
        with open(_file, mode=mode, encoding="UTF-8", errors="ignore") as f:
            f.write(content)

    def read(self, _file):
        """
        Read the _file and return the content
        > _file = name of the file
        """
        #Read the _file
        with open(_file, mode="r", encoding="UTF-8", errors="ignore") as f:
            return f.read()

    def is_news(self, _file, title_list, description_list, link_list, FeedRSSContent):
        """
        Return the title_list, description_list and link_list of the news
        > _file = Name of the file, end of the url path
        > title_list = list of all title
        > description_list = list of all description
        > link_list = list of all link
        """
        #List of News
        news_title = list()
        news_description = list()
        news_link = list()
        #Booleen var for decide if the news is new
        real_new_news = list()
        #Get the path of the file
        path = os.path.join(self.feedrss_path, _file)
        #Verify if the file exist
        if os.path.isfile(path) is False:
            #If not write into the new file and return all title, description and link
            self.write(_file, "w", FeedRSSContent)
            return title_list, description_list, link_list

        #If the file exist get the content and compare to the actual title, description and link
        content = self.read(_file)
        #Get old title, description and link
        old_title, old_description, old_link = self.get_news(content)

        #Compare actual with old news
        for news in range(title_list.__len__()):
            #Old News
            for new_news in range(old_title.__len__()):
                if title_list[news] == old_title[new_news] and description_list[news] == old_description[new_news] and link_list[news] == old_link[new_news]:
                    real_new_news.append(False)
                else:
                    real_new_news.append(True)

            #Add news if real new news
            if False not in real_new_news:
                news_title.append(title_list[news])
                news_description.append(description_list[news])
                news_link.append(link_list[news])

        #Write the new content
        self.write(_file, "w", FeedRSSContent)

        #Return real news
        return news_title, news_description, news_link

    def embeded_msg(self, title, content, link):
        """
        Create the embeded message and send it.
        """
        #Set the title, desciption et couleur sur la gauche
        news = discord.Embed(title="Flux RSS", description="News :", color=0x00ff00)
        #Set le nom du bot et son avatar
        news.set_author(name=self.bot_username, icon_url=self.bot.user.avatar_url)
        #Set la description de la commande rapport de la date
        content = content + "\n" + link
        news.add_field(name=title, value=content, inline=False)
        #Affichage de la personne qui a genere l'help
        news.set_footer(text="Generate by @{0}".format(self.bot_username))

        return news

    async def feedrss(self, cwd, url):
        """
        Get the news and send it to the channel.
        > cwd = Current Working Directory
        > url = URL of the FeedRSS
        """
        self.cwd = cwd
        self.url = url
        #Create the folder with feedrss contains
        self.mkdir("feedrss")
        #Get the name file
        self.file = urlparse(self.url).path.split("/")[-1]
        self.file = os.path.join(self.feedrss_path, self.file)

        while not self.bot.is_closed():
            #Get the content of the news
            title_list, description_list, link_list, FeedRSSContent = self.get_news()
            #Verify if the news already exist, and get the title, description and link
            news_title, news_description, news_link = self.is_news(self.file, title_list, description_list, link_list, FeedRSSContent)
            #Verify if he have more than zero news
            if news_title.__len__() > 0:
                #Send the news for all title, description and link
                for news in range(news_title.__len__()):
                    #Get the embeded message
                    message = self.embeded_msg(news_title[news], news_description[news], news_link[news])
                    #Send the message
                    await self.rss_channel.send(embed=message)
            #Wait before next verification
            await asyncio.sleep(WAIT_NEW_NEWS)
