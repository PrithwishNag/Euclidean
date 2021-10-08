import utils


database = "euclidean.db"
utils.connection.initiate(database)
# utils.playlistUtils.addPlaylist("XXX#5678", "doneout")
# utils.playlistUtils.delPlaylist("Bobochan#5678", "MyPlaylist")
# print(utils.playlistUtils.getPlaylists("XXX#5678"))
ob = utils.playlistUtils("Bobochan1#5678", "MyPlaylist")
