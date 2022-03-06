
import sqlite3
import os

from fts.Utils import database_invoke
from const import SQLITE_CREATE_DATABASE, \
    SQLITE_SELECT_NEWS_EXISTS, SQLITE_INSERT_NEWS, \
        SQLITE_DELETE_NEWS

class Database:

    """
    Instance of Database
    """

    def __init__(self, path, db_name):
        """
        Instance few variables and create database if not exists
        @param => str: `path`: Path to the folder who the database is or are going to was write
        @param => str: `db_name`: Name of the database
        """
        self.path = path
        self.db_name = db_name
        # Full path to the db folder + file name
        self.full_path = os.path.join(self.path, self.db_name)

        # Check if the database exists
        if not os.path.isfile(self.full_path):
            # If not create database
            self.CreateDatabase()


    def ConnectDatabase(self):
        """
        Connect to the database and set a cursor
        """
        self.conn = sqlite3.connect(self.full_path)
        self.cursor = self.conn.cursor()


    def CloseDatabase(self):
        """
        Commit and close connection to the database
        """
        # Save the changes
        self.conn.commit()

        # Close the connection
        self.conn.close()

        # Unset variable
        self.conn, self.cursor = None, None


    @database_invoke
    def CreateDatabase(self):
        """
        Create the database using the full_path variable
        """
        # Create table
        self.cursor.execute(SQLITE_CREATE_DATABASE)


    @database_invoke
    def isNewsExists(self, root, name, title, hash_description, link):
        """
        Return true if the news exists
        @param => str: `title`: Title of the news.
        @param => str: `hash_description`: sha256 hexdigest of the description.
        @param => str: `link`: Link of the news.
        """
        # Arguments
        args = tuple(locals().values())[1:]

        # Execute the query
        self.cursor.execute(SQLITE_SELECT_NEWS_EXISTS, args)
        # Get the response
        result = self.cursor.fetchone()

        # Check the result
        if result is None:
            return False
        return True


    @database_invoke
    def AddNews(self, root, name, title, hash_description, link):
        """
        @param => str: `root`: root name set in const.
        @param => str: `name`: Name set in const.
        @param => str: `title`: Title of the news.
        @param => str: `hash_description`: sha256 hexdigest of the description.
        @param => str: `link`: link of the news.
        """
        # Arguments
        args = tuple(locals().values())[1:]

        # Execute the query
        self.cursor.execute(SQLITE_INSERT_NEWS, args)
    

    @database_invoke
    def DeleteEntries(self, root, name):
        """
        @param => str: `root`: root name set by the user in const.
        @param => str: `name`: name of the subsection set by the user in const.
        """
        # Arguments
        args = tuple(locals().values())[1:]

        # Execute the query
        self.cursor.execute(SQLITE_DELETE_NEWS, args)
