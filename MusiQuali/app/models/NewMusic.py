class Music:
    def __init__(self, id, title, path, duration):
        self.id = id
        self.title = title
        self.path = path
        self.duration = duration

    def to_dict(self):
        return {
            "id": self.id,
            "title": self.title,
            "path": self.path,
            "duration": self.duration
        }