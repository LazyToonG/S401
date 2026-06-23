class Planning:
    def __init__(self, idPlanning=None, idPlaylist=None, idMSG=None,
                 StartTime=None, idEntreprise=1):
        self.idPlanning = idPlanning
        self.idPlaylist = idPlaylist
        self.idMSG = idMSG
        self.StartTime = StartTime  # ISO 8601 string, e.g. "2026-06-22T08:30:00"
        self.idEntreprise = idEntreprise
