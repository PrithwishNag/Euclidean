import sqlite3
import utils


def create_connection(db_file):
    return utils.connection.initiate(db_file)


def create_table(conn, sql):
    try:
        c = conn.cursor()
        c.execute(sql)
    except Exception as e:
        print(e)


def main():
    database = "euclidean.db"

    sql_table = {
        "user": """CREATE TABLE IF NOT EXISTS user (
                    id text PRIMARY KEY
                );""",
        "user-playlist": """CREATE TABLE IF NOT EXISTS userplaylist (
                            id text PRIMARY KEY,
                            user_id text NOT NULL,
                            playlist_name text NOT NULL,
                            FOREIGN KEY (user_id) REFERENCES user (id),
                            UNIQUE(user_id, playlist_name)
                        );""",
        "song": """CREATE TABLE IF NOT EXISTS song (
                    id text PRIMARY KEY,
                    title text NOT NULL,
                    channel text NOT NULL,
                    url text NOT NULL
                );""",
        "playlist-song": """CREATE TABLE IF NOT EXISTS playlistsong (
                            id text PRIMARY KEY,
                            user_playlist_id text NOT NULL,
                            song_id text NOT NULL,
                            FOREIGN KEY (user_playlist_id) REFERENCES userplaylist (id),
                            FOREIGN KEY (song_id) REFERENCES song (id),
                            UNIQUE(user_playlist_id, song_id)
                        );""",
    }

    # create a database connection
    conn = create_connection(database)

    for sql in sql_table.values():
        create_table(conn, sql)


if __name__ == "__main__":
    main()
