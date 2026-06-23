import json
import os
from app import app

class RequeteDAO:
    def __init__(self):
        # Le fichier sera stocké dans ton dossier static/data/
        self.filepath = os.path.join(app.static_folder, 'data', 'requetes.json')
        
        # Si le fichier n'existe pas encore, on le crée avec un dictionnaire vide
        if not os.path.exists(self.filepath):
            with open(self.filepath, 'w', encoding='utf-8') as f:
                json.dump({}, f)

    def lire_json(self):
        with open(self.filepath, 'r', encoding='utf-8') as f:
            return json.load(f)

    def ecrire_json(self, data):
        with open(self.filepath, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=4, ensure_ascii=False)

    def ajouter_requete(self, demandeur, mail, type_req, message, role=None, entreprise=None, mdp=None, nouveau_role=None):
        data = self.lire_json()
        
        # Générer un nouvel ID (le plus grand ID existant + 1)
        if data:
            nouvel_id = str(max([int(k) for k in data.keys()]) + 1)
        else:
            nouvel_id = "1"
        
        data[nouvel_id] = {
            "demandeur": demandeur,
            "mail": mail,
            "type": type_req,
            "role": role,
            "entreprise": entreprise,
            "mdp": mdp,
            "message": message,
            "statut": "en_attente",
            "nouveau_role": nouveau_role
        }
        
        self.ecrire_json(data)
        return True