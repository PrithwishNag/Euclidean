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

    def addSong(self, song):
        try:
            c = connection.conn.cursor()
            c.execute(
                "SELECT id FROM song WHERE title=? AND channel=?",
                (
                    song["title"],
                    song["channel"],
                ),
            )
            song_id = c.fetchone()
            if song_id is not None:
                return song_id[0]

            unique_id = str(uuid.uuid1().int)
            c.execute(
                "INSERT INTO song(id, title, channel, url) VALUES(?, ?, ?, ?)",
                (
                    unique_id,
                    song["title"],
                    song["channel"],
                    song["url"],
                ),
            )
            connection.conn.commit()
            return unique_id
        except Exception as e:
            print(e)
            return None

    def addSongToPlaylist(self, song):
        try:
            c = connection.conn.cursor()
            unique_id = str(uuid.uuid1().int)
            song_id = self.addSong(song)
            c.execute(
                "SELECT id FROM userplaylist WHERE user_id=? AND playlist_name=?",
                (
                    self.author,
                    self.playlist,
                ),
            )
            user_playlist_id = c.fetchone()[0]
            c.execute(
                "INSERT INTO playlistsong(id, user_playlist_id, song_id) VALUES(?, ?, ?)",
                (
                    unique_id,
                    user_playlist_id,
                    song_id,
                ),
            )
            connection.conn.commit()
            return True
        except Exception as e:
            print(e)
            return False

    def getSongs(self):
        try:
            c = connection.conn.cursor()
            c.execute(
                """SELECT * FROM song WHERE id IN
                (SELECT song_id FROM playlistsong WHERE user_playlist_id=
                (SELECT id FROM userplaylist WHERE user_id=? and playlist_name=?))""",
                (
                    self.author,
                    self.playlist,
                ),
            )
            rows = c.fetchall()
            return rows
        except Exception as e:
            print(e)
            return []

    def removeSong(self, song_id):
        try:
            c = connection.conn.cursor()
            c.execute(
                """DELETE FROM playlistsong WHERE song_id=? AND user_playlist_id=
                (SELECT id FROM userplaylist WHERE user_id=? AND playlist_name=?)""",
                (
                    song_id,
                    self.author,
                    self.playlist,
                ),
            )
            connection.conn.commit()
            return True
        except Exception as e:
            print(e)
            return False
