import sqlite3


class connection:
    conn = None

    def initiate(db_file):
        try:
            connection.conn = sqlite3.connect(db_file)
        except Exception as e:
            print(e)
        return connection.conn


class playlistUtils:
    def __init__(self, author, playlist):
        self.author = author
        self.playlist = playlist  # Selected playlist

    @staticmethod
    def addPlaylist(author):
        try:
            c = connection.conn.cursor()
            c.execute("")
            return True
        except Exception as e:
            return False

    @staticmethod
    def getPlaylists(author):
        try:
            c = connection.conn.cursor()
            return c.execute("")
        except Exception as e:
            return []

    def addSong(self, song):
        pass

    def getSongs(self):
        pass
