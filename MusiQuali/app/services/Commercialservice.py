
from app.models.Playlist import Playlist
from app.DAO.PlaylistDAO import PlaylisteDAO


class CommercialService:
    """

    """

    def __init__(self):
        self.dao = PlaylisteDAO()

    def get_all_commercials(self):
        """Retourne tous les commerciaux existants."""
        return self.dao.get_all()

    def get_commercial(self, commercial_id):
        """Retourne un commercial par son id, ou None si il n'existe pas."""
        return self.dao.get(commercial_id)

    def create_commercial(self, title, idUtilisateur=1, idPlanning=1):
        """
        Crée un nouveau commercial.
        Lève une ValueError si le titre est vide.
        """
        if not title or not title.strip():
            raise ValueError("Le titre du commercial ne peut pas être vide.")

        commercial = Playlist(
            title=title.strip(),
            idUtilisateur=idUtilisateur,
            idPlanning=idPlanning
        )
        self.dao.create(commercial)
        return commercial

    def rename_commercial(self, commercial_id, new_title):
        """Renomme un commercial existant."""
        commercial = self.dao.get(commercial_id)
        if commercial is None:
            raise ValueError(f"Commercial {commercial_id} introuvable.")

        if not new_title or not new_title.strip():
            raise ValueError("Le titre du commercial ne peut pas être vide.")

        commercial.title = new_title.strip()
        self.dao.create(commercial)  # create() fait un UPDATE si idPlaylist existe déjà
        return commercial

    def delete_commercial(self, commercial_id):
        """
        Supprime un commercial.
        #TODO: s'assurer ici (ou en amont) que les musiques associées
        # ont déjà été supprimées, cf. commentaire du DAO.
        """
        commercial = self.dao.get(commercial_id)
        if commercial is None:
            raise ValueError(f"Commercial {commercial_id} introuvable.")

        self.dao.delete(commercial_id)