from app.DAO.PlaylistDAO import PlaylisteDAO
from app.DAO.MusicDAO import MusicDAO
import os
from mutagen.mp3 import MP3
from werkzeug.utils import secure_filename
from app import app
from flask import session
from app.DAO.RelationPlaylistMusicDAO import RelationPlaylistMusicDAO


class MarketingService:

    def __init__(self):
        self.playlistDAO = PlaylisteDAO()
        self.musicDAO = MusicDAO()
        self.relationDAO = RelationPlaylistMusicDAO() 

    def get_marketing_data(self):
        return {
        "playlists": self.get_playlists_with_stats(),
        "musiques": self.get_all_musics()
            
        }

 # Playlistes       

    def get_playlists(self):
        return self.playlistDAO.get_all()

    def get_playlists_with_stats(self):
        """Retourne les playlists enrichies avec nb_musiques et duree_totale."""
        playlists = self.playlistDAO.get_all()
        all_musics = {m.idMusique: m for m in self.musicDAO.get_musiques()}
        result = []
        for p in playlists:
            rows = self.relationDAO.get_musiques_by_playlist(p.idPlaylist)
            nb = len(rows)
            duree_totale = sum(
                all_musics[r["idMusique"]].duree
                for r in rows if r["idMusique"] in all_musics
            ) + nb  # +1s de pause par musique
            result.append({
                "idPlaylist": p.idPlaylist,
                "title": p.title,
                "idUtilisateur": p.idUtilisateur,
                "idPlanning": p.idPlanning,
                "nb_musiques": nb,
                "duree_totale": duree_totale
            })
        return result

    def get_playlist_tracks(self, playlist_id):
        """Retourne la liste des musiques associées à une playlist."""
        playlist = self.playlistDAO.get(playlist_id)
        if not playlist:
            return []

        ids = self.playlistDAO._str_to_ids(getattr(playlist, "musiques", None))
        all_musics = {m.idMusique: m for m in self.musicDAO.get_all()}

        return [all_musics[i] for i in ids if i in all_musics]

    def add_playlist(self, title):
        from app.models.Playlist import Playlist
        idUtilisateur = session['idUtilisateur']  # adapte la clé si nécessaire
        playlist = Playlist(idPlaylist=None, title=title, idUtilisateur=idUtilisateur, idPlanning=1)
        self.playlistDAO.create(playlist)
        return playlist

    def delete_playlist(self, idPlaylist):
        self.relationDAO.remove_all_from_playlist(idPlaylist)
        self.playlistDAO.delete(idPlaylist)


# Musiques

    
    def get_all_musics(self):
        return self.musicDAO.get_musiques()

    def add_music(self, nomMusique, duree, idEntreprise):
        return self.musicDAO.create(nomMusique, duree, idEntreprise)

    def delete_music(self, idMusique):
        music = self.musicDAO.get_by_id(idMusique)
        #!!!! todo, virer le mp3 de allmusics--- fait
        if music:
            filepath = os.path.join(app.static_folder, "AllMusics", music.nomMusique)
            if os.path.exists(filepath):#rm mp3 du dossier
                os.remove(filepath)

        self.musicDAO.delete(idMusique) #rm objet de la bd

    
    def save_music_files(self, files, idEntreprise):
    #Sauvegarde plusieurs fichiers mp3, retourne la liste des Music créées.
        created = []
        for file in files:
            if file and file.filename:
                created.append(self.save_music_file(file, idEntreprise))
        return created


    def save_music_file(self, file, idEntreprise):
    
   # Sauvegarde le fichier mp3 dans app/static/AllMusics
    #et enregistre la musique en base de données.
    #Retourne l'objet Music créé.

        filename = secure_filename(file.filename)

        folder = os.path.join(app.static_folder, "AllMusics")
        os.makedirs(folder, exist_ok=True)




        # Vérifie les collisions de noms et ajoute (n) si nécessaire
        base, ext = os.path.splitext(filename)
        candidate = filename
        counter = 1
        while os.path.exists(os.path.join(folder, candidate)):
            candidate = f"{base}({counter}){ext}"
            counter += 1

        


        filename = candidate
        nomMusique = filename

        filepath = os.path.join(folder, filename)
        file.save(filepath)

        # Extraction de la durée (en secondes, arrondie)
        try:
            audio = MP3(filepath)
            duree = int(audio.info.length)
        except Exception:
            duree = 0

        return self.musicDAO.create(nomMusique, duree, idEntreprise)



# --- RELATION PLAYLIST / MUSIQUE ---

    def add_music_to_playlist(self, idPlaylist, idMusique, position):
        """Ajoute une musique à une playlist à une position donnée."""
        self.relationDAO.add(idPlaylist, idMusique, position)

    def remove_music_from_playlist(self, idCouple):
        """Retire une entrée de playlist par son idCouple."""
        self.relationDAO.remove(idCouple)

    def get_musiques_by_playlist(self, idPlaylist):
        """Retourne les musiques d'une playlist avec idCouple et position."""
        rows = self.relationDAO.get_musiques_by_playlist(idPlaylist)
        musiques = []
        for row in rows:
            m = self.musicDAO.get_by_id(row["idMusique"])
            if m is not None:
                musiques.append({
                    'idCouple': row["idCouple"],
                    'idMusique': m.idMusique,
                    'nomMusique': m.nomMusique,
                    'duree': m.duree,
                    'position': row["position"]
                })
        return musiques
    
    def save_positions(self, positions):
        """
        Met à jour la position de chaque entrée playlist-musique.
        positions : liste de dicts {idCouple, position}
        """
        for entry in positions:
            self.relationDAO.update_position(entry["idCouple"], entry["position"])

    # def save_playlist_composition(self, idPlaylist, idMusiques):
    #     """
    #     Sauvegarde la composition complète d'une playlist.
    #     idMusiques : liste d'idMusique à associer.
    #     Vide d'abord la playlist puis réinsère.
    #     """
    #     self.relationDAO.remove_all_from_playlist(idPlaylist)
    #     for idMusique in idMusiques:
    #         self.relationDAO.add(idPlaylist, idMusique)