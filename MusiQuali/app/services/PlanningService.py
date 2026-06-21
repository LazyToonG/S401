from app.models.Planning import Planning
from app.DAO.PlanningDAO import PlanningDAO


class PlanningService:
 

    def __init__(self):
        self.dao = PlanningDAO()

    def get_all(self, idEntreprise=1):
        """Retourne tout le planning pour une entreprise (état initial des calendriers)."""
        return self.dao.get_all(idEntreprise)

    def sync(self, boxes, idEntreprise=1):
        """
    
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
