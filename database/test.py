import utils


database = "euclidean.db"
utils.connection.initiate(database)
# utils.playlistUtils.addPlaylist("Bobochan#5678", "MyPlaylist")
# utils.playlistUtils.delPlaylist("Bobochan#5678", "MyPlaylist")
# print(utils.playlistUtils.getPlaylists("XXX#5678"))
ob = utils.playlistUtils("BoBoChan#1613", "gg")
song = {"title": "need to know", "channel": "doja cat", "url": "dkjadbakd"}
print(ob.removeSong("289339708289089111163753847614950882120"))
# print(ob.addSongToPlaylist(song))
