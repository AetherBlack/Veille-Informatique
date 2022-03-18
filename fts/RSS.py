
import discord


class RSS:

    def __init__(self, root: str, section: dict) -> None:
        """
        @param => str: `root`: Root name of the section set in `const/`
        @param => dict: `section`: Sections of the root name
        """
        # Args
        self.root = root
        self.section = section

        # Get all
        self.getInformationsFromSection()

    def getInformationsFromSection(self) -> None:
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

    def getCustomParameters(self) -> None:
        """
        Get custom parameters from `self.section`
        """
        # Color
        self.getCustomColor()
        # Filter
        self.getCustomFilter()

    def getCustomColor(self) -> None:
        """
        Get color from the custom parameters
        """
        # Get customisation
        if "custom" in self.section.keys():
            # Check color
            if "color" in self.section["custom"].keys():
                if self.section["custom"]["color"] in dir(discord.Color):
                    self.color = getattr(discord.Color, self.section["custom"]["color"])()
                else:
                    print(f"[!] The Color {self.section['custom']['color']} doesn't exists in `discord.Color` ! Set default color instead.")
                    self.color = False
            else:
                self.color = False
        else:
            self.color = False

    def getCustomFilter(self) -> None:
        """
        Get filter from the custom parameters
        """
        # Get custom
        if "custom" in self.section.keys():
            # Check filter
            if "filter" in self.section["custom"].keys():
                self.filter = self.section["custom"]["filter"]
            else:
                self.filter = False
        else:
            self.filter = False
