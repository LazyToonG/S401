
class Playliste:
    def __init__(self, title, id=None, music_ids=None):
        self.id = id
        self.title = title
        self.music_ids = music_ids if music_ids is not None else []
        
        #dans le dao je transforme en "id|id|etc" pour la bd
        #un objet peut avoir en attribut un autre (= composition si il en dépend sinon agregation)
        #au final je m'en sers pas mais c utile a savoir lol
  
    def addMusique(self, music_id: int):
        self.music_ids.append(music_id)




    