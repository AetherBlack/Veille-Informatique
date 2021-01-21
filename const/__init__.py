# Token
TOKEN = "YOUR_BOT_TOKEN"

# CHANNEL FLUX RSS -> NOTIF ID
CHANNEL_RSS = INT_CHANNEL

# WAIT UNTIL NEW VERIFICATION NEWS
WAIT_UNTIL_NEW_CHECK = 60 * 60#Each hours

# Flux RSS
JSON_RSS = {
  "Google": [
    {
      "name": "WPA-3",
      "description": "WPA-3 English Feed",
      "clean": "1d",
      "link": [
        "https://www.google.com/alerts/feeds/10044275366631447452/5208661666063475899",
      ]
    },
    {
      "name": "CyberSecurity",
      "decription": "CyberSecurity English & French Feed",
      "clean": "1d",
      "link": [
        "https://www.google.fr/alerts/feeds/02095771238174224890/10101746411290367862",# English
        "https://www.google.fr/alerts/feeds/02095771238174224890/2639999938357813092"# French
      ]
    }
  ],
  "Reddit": [
    {
      "name": "Netsec",
      "description": "Netsec feed of reddit",
      "clean": "12h",
      "link": [
        "https://www.reddit.com/r/netsec/.rss"
      ]
    }
  ],
  "ANSSI": [
    {
      "name": "CERT-FR",
      "description": "Rapport du CERT-FR",
      "clean": "365d",
      "link": [
        "https://www.cert.ssi.gouv.fr/feed/"
      ]
    }
  ]
}

# Database Folder Name
SQLITE_FOLDER_NAME = "db"

# Database File Name
SQLITE_FILE_NAME = "fluxrss.sqlite"

# Database requests
SQLITE_CREATE_DATABASE = """
    CREATE TABLE IF NOT EXISTS news (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        root text NOT NULL,
        name text NOT NULL,
        title text NOT NULL,
        hash_description text NOT NULL,
        link text NOT NULL
    );
"""

SQLITE_SELECT_NEWS_EXISTS = """
    SELECT 1
    FROM news
    WHERE root=?
    AND name=?
    AND title=?
    AND hash_description=?
    AND link=?;
"""

SQLITE_INSERT_NEWS = """
    INSERT INTO news (
        root, name, title, hash_description, link
    ) VALUES (
        ?, ?, ?, ?, ?
    );
"""

SQLITE_DELETE_NEWS = """
      DELETE FROM news
      WHERE root=?
      AND name=?;
"""
