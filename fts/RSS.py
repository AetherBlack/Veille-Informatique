
import discord

class RSS:


    def __init__(self, root: str, section: dict):
        """
        @param => str: `root`: Root name of the section set in `const/`
        @param => dict: `section`: Sections of the root name
        """
        # Args
        self.root = root
        self.section = section

        # Get all
        self.getInformationsFromSection()


    def getInformationsFromSection(self):
        """
        Get informations from `self.section`
        """
        # Get custom parameters like color and other
        self.getCustomParameters()

        # Get the name of the section
        self.name = self.section["name"]

        # Get the time until the cleaning of the database for the root and name given
        self.wait_time = self.section["clean"]

        # Get link
        self.link = self.section["link"]


    def getCustomParameters(self):
        """
        Get custom parameters from `self.section`
        """
        # Color
        self.getCustomColor()
    

    def getCustomColor(self):
        """
        Get color from the custom parameters
        """
        # Get customisation
        if "custom" in self.section.keys():
            # Check color
            if "color" in self.section["custom"].keys():
                self.color = getattr(discord.Color, self.section["custom"]["color"])()
            else:
                self.color = False
        else:
            self.color = False
