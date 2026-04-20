from app.DAO.PlaylistDAO import PlaylisteDAO
from app.DAO.MusicDAO import MusicDAO

class PlaylistService:
    def __init__(self):
        self.playlist_dao = PlaylisteDAO()
        self.music_dao = MusicDAO()

    def get_all_playlists(self):
        return self.playlist_dao.get_all()

    def create_playlist(self, name):
        self.playlist_dao.create(name)

    def get_playlists_api_data(self):
        playlists = self.playlist_dao.get_all()
        data = {}
        for pl in playlists:
            musics_data = []
            for music_id in pl.music_ids:
                m = self.music_dao.get_by_id(music_id)
                if m:
                    musics_data.append({
                        'name': m.title, 
                        'artist': "", 
                        'path': m.path, 
                        'duration': m.duration
                    })
            data[pl.title] = musics_data
        return data

service_playlist = PlaylistService()