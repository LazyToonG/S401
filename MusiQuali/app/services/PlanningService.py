from app.models.Planning import Planning
from app.DAO.PlanningDAO import PlanningDAO


class PlanningService:
    """
    Couche service pour le planning (calendrier des commerciaux/playlists
    et calendrier des messages).

    Le front envoie l'état complet du calendrier au moment du Save :
    une liste de "boxes", chacune avec soit idPlaylist soit idMSG (jamais les
    deux), un StartTime (ISO 8601), et optionnellement idPlanning si la box
    existe déjà en bd (auquel cas c'est un update, sinon une création).

    Le service calcule le diff par rapport à ce qui est en bd : les lignes
    absentes du payload sont supprimées, les nouvelles sont insérées, celles
    avec idPlanning connu sont mises à jour.
    """

    def __init__(self):
        self.dao = PlanningDAO()

    def get_all(self, idEntreprise=1):
        """Retourne tout le planning pour une entreprise (état initial des calendriers)."""
        return self.dao.get_all(idEntreprise)

    def sync(self, boxes, idEntreprise=1):
        """
        boxes: liste de dicts, chacun avec les clés possibles:
            - idPlanning (int ou None) : None si la box n'existe pas encore en bd
            - idPlaylist (int ou None)
            - idMSG (int ou None)
            - StartTime (str ISO 8601)

        Retourne la liste des Planning à jour (avec idPlanning rempli pour les
        nouvelles entrées), pour que le front puisse re-synchroniser ses boxes.
        """
        existing = self.dao.get_all(idEntreprise)
        existing_ids = {p.idPlanning for p in existing}
        incoming_ids = set()

        results = []

        for box in boxes:
            idPlaylist = box.get("idPlaylist")
            idMSG = box.get("idMSG")

            if (idPlaylist is None) == (idMSG is None):
                # garde-fou : une box doit avoir exactement l'un des deux
                raise ValueError(
                    "Chaque box doit référencer soit idPlaylist soit idMSG (jamais les deux, ni aucun)."
                )

            start_time = box.get("StartTime")
            if not start_time:
                raise ValueError("StartTime est requis pour chaque box.")

            planning = Planning(
                idPlanning=box.get("idPlanning"),
                idPlaylist=idPlaylist,
                idMSG=idMSG,
                StartTime=start_time,
                idEntreprise=idEntreprise
            )

            saved = self.dao.create(planning)  # create() gère insert ou update
            incoming_ids.add(saved.idPlanning)
            results.append(saved)

        # Supprime en bd ce qui n'est plus présent côté calendrier
        removed_ids = existing_ids - incoming_ids
        for planning_id in removed_ids:
            self.dao.delete(planning_id)

        return results

    def delete(self, planning_id):
        """Supprime une entrée précise du planning."""
        self.dao.delete(planning_id)
