
import sqlite3
import os

from const import SQLITE_CREATE_DATABASE, \
    SQLITE_SELECT_NEWS_EXISTS, SQLITE_INSERT_NEWS

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
        conn = sqlite3.connect(self.full_path)
        cursor = conn.cursor()
        return conn, cursor


    def CloseDatabase(self, conn):
        """
        Commit and close connection to the database
        """
        # Save the changes
        conn.commit()

        # Close the connection
        conn.close()


    def CreateDatabase(self):
        """
        Create the database using the full_path variable
        """
        # Get connection and cursor 
        conn, cursor = self.ConnectDatabase()

        # Create table
        cursor.execute(SQLITE_CREATE_DATABASE)

        # Close the connection
        self.CloseDatabase(conn)


    def isNewsExists(self, title, hash_description, link):
        """
        Return true if the news exists
        @param => str: `title`: Title of the news.
        @param => str: `hash_description`: sha256 hexdigest of the description.
        @param => str: `link`: Link of the news.
        """
        # Arguments
        args = (title, hash_description, link, )
        # Connect to the database
        conn, cursor = self.ConnectDatabase()

        # Execute the query
        result = cursor.execute(SQLITE_SELECT_NEWS_EXISTS, args)

        # Close connection
        self.CloseDatabase(conn)

        # Check the result
        if result is None:
            return False
        return True


    def AddNews(self, root, name, title, hash_description, link):
        """
        @param => str: `root`: root name set in const.
        @param => str: `name`: Name set in const.
        @param => str: `title`: Title of the news.
        @param => str: `hash_description`: sha256 hexdigest of the description.
        @param => str: `link`: link of the news.
        """
        # Arguments
        args = (root, name, title, hash_description, link,)
        # Connect to the database
        conn, cursor = self.ConnectDatabase()

        # Execute the query
        cursor.execute(SQLITE_INSERT_NEWS, args)

        # Close connection
        self.CloseDatabase(conn)
