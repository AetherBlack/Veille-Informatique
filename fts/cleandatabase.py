
from datetime import timedelta
from threading import Thread

import time

from fts.database import Database


class CleanDatabase(Thread):

    """
    Instance of CleanDatabase
    """

    def __init__(self, root: str, name: str, wait_time: int, db_path: str, db_name: str):
        """
        @param => str: `root`: root name set in const.
        @param => str: `name`: name set in the subsection of root.
        @param => int: `wait_time`: Waiting time before clean.
        @param => str: `db_path`: Path to the database folder. 
        @param => str: `db_name`: Name of the database file.
        """
        # Threading
        Thread.__init__(self)
        # Database
        self.database = Database(db_path, db_name)
        # Variable for clean
        self.root = root
        self.name = name
        self.wait_time = 0
        # Convert the clean time to wait_time
        tmp_time = wait_time.split(",")

        # For each split
        for t in tmp_time:

            # Add seconds
            if "s" in t:
                t = int(t.replace("s", ""))
                self.wait_time += t

            # Convert minutes to seconds and add it to the var
            elif "m" in t:
                t = int(t.replace("m", ""))
                self.wait_time += timedelta(minutes=t).total_seconds()

            # Convert hours to seconds and add it to the var
            elif "h" in t:
                t = int(t.replace("h", ""))
                self.wait_time += timedelta(hours=t).total_seconds()

            # Convert days to seconds and add it to the var
            elif "d" in t:
                t = int(t.replace("d", ""))
                self.wait_time += timedelta(days=t).total_seconds()

            # Convert weeks to seconds and add it to the var
            elif "w" in t:
                t = int(t.replace("w", ""))
                self.wait_time += timedelta(weeks=t).total_seconds()

    def run(self):
        """
        Function who clean the database
        """
        while True:
            # Wait the clean time defined by the user
            time.sleep(self.wait_time)

            # Now clean
            self.database.DeleteEntries(self.root, self.name)
