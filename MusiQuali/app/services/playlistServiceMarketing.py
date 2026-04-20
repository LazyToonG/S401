from app.DAO.PlaylistDAO import PlaylisteDAO
from app.models.Playliste import Playliste
from app.DAO.MusicDAO import MusicDAO

class PlaylistService:
    def __init__(self):
        self.dao = PlaylisteDAO()

    def create_playlist(self, title):
        p = Playliste(title=title)
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

        playlist.addMusique(music_id)
        self.dao.insert(playlist)

    def musics_in_playlist(self, playlist_id):
        musicList=[]
        a=PlaylisteDAO()
        b=MusicDAO()
        c=a.get(playlist_id)
        for i in c.music_ids:
            d=b.get_by_id(i)
            musicList.append(d)
            
        return musicList

    def delete_playlist(self, playlist_id):
        a=PlaylisteDAO()
        a.delete(playlist_id)