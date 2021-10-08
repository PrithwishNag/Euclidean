import sqlite3
import uuid


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

    def exists(self):
        try:
            c = connection.conn.cursor()
            c.execute(
                "SELECT id FROM userplaylist WHERE user_id=? AND playlist_name=?",
                (
                    self.author,
                    self.playlist,
                ),
            )
            if c.fetchall() == []:
                return False
            return True
        except Exception as e:
            print(e)
            return False

    @staticmethod
    def addPlaylist(author, playlist):
        try:
            c = connection.conn.cursor()
            unique_id = str(uuid.uuid1().int)
            c.execute(
                "INSERT INTO userplaylist(id, user_id, playlist_name) VALUES(?, ?, ?)",
                (unique_id, author, playlist),
            )
            connection.conn.commit()
            return True
        except Exception as e:
            print(e)
            return False

    @staticmethod
    def delPlaylist(author, playlist):
        try:
            c = connection.conn.cursor()
            c.execute(
                "DELETE FROM userplaylist WHERE user_id=? AND playlist_name=?",
                (
                    author,
                    playlist,
                ),
            )
            connection.conn.commit()
            return True
        except Exception as e:
            print(e)
            return False

    @staticmethod
    def getPlaylists(author):
        try:
            c = connection.conn.cursor()
            c.execute(
                "SELECT playlist_name FROM userplaylist WHERE user_id=?", (author,)
            )
            rows = c.fetchall()
            return rows
        except Exception as e:
            print(e)
            return []

    def addSong(self, song):
        pass

    def getSongs(self):
        pass
