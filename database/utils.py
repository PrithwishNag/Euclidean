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

    @staticmethod
    def addPlaylist(author, playlist):
        try:
            c = connection.conn.cursor()
            unique_id = str(uuid.uuid1().int)
            c.execute(
                "INSERT INTO playlist(id, name) VALUES(?, ?)",
                (
                    unique_id,
                    playlist,
                ),
            )
            c.execute(
                "INSERT INTO userplaylist(user_id, playlist_id) VALUES(?, ?)",
                (
                    author,
                    unique_id,
                ),
            )
            connection.conn.commit()
            return True
        except Exception as e:
            print(e)
            return False

    # @staticmethod
    # def delPlaylist(author, playlist):
    #     try:
    #         c = connection.conn.cursor()
    #         c.execute("")
    #         c.execute(
    #             "INSERT INTO userplaylist(user_id, playlist_id) VALUES(?, ?)",
    #             (
    #                 author,
    #                 unique_id,
    #             ),
    #         )
    #         connection.conn.commit()
    #         return True
    #     except Exception as e:
    #         print(e)
    #         return False

    @staticmethod
    def getPlaylists(author):
        try:
            c = connection.conn.cursor()
            return c.execute("")
        except Exception as e:
            print(e)
            return []

    def addSong(self, song):
        pass

    def getSongs(self):
        pass
