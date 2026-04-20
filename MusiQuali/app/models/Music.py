class Music:
    def __init__(self, id, title, path, duration):
        self.id = id
        self.title = title
        self.path = path
        self.duration = int(duration)
        self.artist = ""  # Initialiser artist par défaut
    
    # Propriétés pour compatibilité avec le template (qui utilise titre et artiste en français)
    @property
    def titre(self):
        return self.title
    
    @property
    def artiste(self):
        return self.artist

