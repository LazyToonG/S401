from app.DAO.PlaylistDAO import PlaylisteDAO
from app.models.Playlist import Playlist
from app.DAO.MusicDAO import MusicDAO
from app.DAO.AjouterDAO import AjouterSqliteDAO as AjouterDAO

class PlaylistService:
    def __init__(self):
        self.dao = PlaylisteDAO()
        self.ajouter_dao = AjouterDAO()

    def create_playlist(self, title):
        p = Playlist(title=title, idUtilisateur=1, idPlanning=1)#enlevez les 1
        self.dao.insert(p)
        return p

    def get_all(self):
        return self.dao.get_all()

    def get_by_id(self, playlist_id):
        return self.dao.get(playlist_id)

    def add_music_to_playlist(self, playlist_id, music_id):
        playlist = self.dao.get(playlist_id)
        if not playlist:
            raise ValueError("Playlist inexistante")

        self.ajouter_dao.add_music_to_playlist(playlist_id, music_id)
        self.dao.insert(playlist)

#ça doit etre fait dans le coté musique et plus playlist
    def musics_in_playlist(self, playlist_id):
        music_list = []

        playlist = self.dao.get(playlist_id)
        if not playlist:
            return []

        music_ids = self.ajouter_dao.getMusicIdsByPlaylist(playlist.idPlaylist)

        for music_id in music_ids:
            music = MusicDAO().get_by_id(music_id)
            music_list.append(music)

        return music_list

    def delete_playlist(self, playlist_id):
        a=PlaylisteDAO()
        a.delete(playlist_id)