from flask import session, request
class Traductionservice():

    def getLangue(self):
        langue_url = request.args.get('lang')
        if langue_url:
            session['langue'] = langue_url
            langue_choisie = langue_url
        else:
            langue_choisie = session.get('langue')

        if langue_choisie not in ['fr', 'en']:
            langue_choisie = 'fr' 
        return langue_choisie
    
    def message_langue(self, message_fr, message_en):
        langue_choisie=Traductionservice.getLangue(self)
        if langue_choisie=='fr':
            message = message_fr
        elif langue_choisie=="en":
            message=message_en
        return message

    def tradIndex(self):
        return {
            'fr': {
                "login" : "Se connecter",
                'titre': "Bienvenue sur Musi-quali, votre plateforme de diffusion sonore",
                'desc_1': "Musi-quali est une plateforme qui vous permettra de diffuser de la musique et des messages sonores dans votre établissement. Vous pouvez préparer à l'avance un planning de musiques et de messages de publicité directement en ligne, faire des annonces quand vous voulez, et notre plateforme marche même en cas de coupure de connexion.",
                'desc_2': "Besoin d'une ambiance sonore dans votre magasin ? Utilisez Musi-quali !",
                'equipe_intro': "Nous somme une équipe d'éudiants en deuxième année en BUT Informatique à l'Universitée Sorbonne Paris Nord.",
                'equipe_liste': "Notre équipe est composée de :"
            },
            'en': {
                "login" : "Login",
                'titre': "Welcome to Musi-quali, your sound broadcasting platform",
                'desc_1': "Musi-quali is a platform that allows you to broadcast music and audio messages in your establishment. You can prepare a schedule of music and advertising messages in advance directly online, make announcements whenever you want, and our platform even works in the event of a connection failure.",
                'desc_2': "Need a sound atmosphere in your store? Use Musi-quali!",
                'equipe_intro': "We are a team of second-year students studying for a Bachelor's degree in Computer Science at Sorbonne Paris Nord University.",
                'equipe_liste': "Our team consists of:"
            }
        }
    
    def tradLogin(self):
        return {
            "fr" : {
                "user" : "Utilisateur",
                "logout" : "Déconnexion",
                "index" : "Accueil",
                "h1" : "Nom d'utilisateur",
                "password" : "Mot de passe",
                "role" : "Rôle",
                "connexion" : "Connexion",
                "create" : "Créer",
                "commercial" : "Commercial (Défaut)",
                "marketing" : "Marketing",
                "admin" : "Administrateur",
                "error" : "Identifiants non valides"
            },

            "en" : {
                "user" : "User",
                "logout" : "Logout",
                "index" : "Home",
                "h1" : "Username",
                "role" : "Role",
                "password" : "Password",
                "connexion" : "Login",
                "create" : "Create",
                "commercial" : "Commercial (Default)",
                "marketing" : "Marketing",
                "admin" : "Administrator",
                "error" : "Invalid Credentials"
            }
        }
    
    def tradAdmin(self):
        return {
            "fr" : {
                "fichier" : "Envoyer des fichiers musiques manuellement",
                "titreRasp" : "Ajouter une Raspberry",
                "nomRasp" : "Quel est l'identifiant/nom de la nouvelle Raspberry que vous voulez insérer ?",
                "ipRasp" : "Quel est l'adresse IP de la nouvelle Raspberry que vous voulez insérer ?",
                "form_nomRasp" : "Entrez l'identifiant de la Raspberry",
                "form_ipRasp" : "Entrez l'adresse IP de la Raspberry",
                "bouton_ajoutRasp" : "Ajouter la Raspberry",
                "user" : "Utilisateur",
                "logout" : "Déconnexion",
                "role" : "Rôle",
                "select_rasp" : "Sélectionner une Raspberry",
                "select" : "Sélectionner",
                "download" : "Télécharger les logs",
                "users" : "Utilisateurs",
                "create_user" : "Créer un utilisateur",
                "name_user" : "Nom d'utilisateur",
                "password" : "Mot de passe",
                "choix_role" : "Choisir un rôle",
                "connexion" : "Connexion",
                "create" : "Créer l'utilisateur",
                "admin" : "Administrateur",
                "recherche" : "Rechercher un utilisateur",
                "recherche_user" : "Utilisateur recherché",
                "search" : "Rechercher",
                "result" : "Résultat",
                "name" : "Nom",
                "supp" : "Supprimer",
                "confirm" : "Confirmer",
                "cancel" : "Annuler"
            },

            "en" : {
                "fichier" : "Manually send music files",
                "titreRasp" : "Add a Raspberry",
                "nomRasp" : "What is the identifier/name of the new Raspberry you want to insert?",
                "ipRasp" : "What is the IP address of the new Raspberry you want to insert?",
                "form_nomRasp" : "Enter the Raspberry identifier",
                "form_ipRasp" : "Enter the Raspberry IP address",
                "bouton_ajoutRasp" : "Add the Raspberry",
                "user" : "User",
                "logout" : "Logout",
                "role" : "Role",
                "select_rasp" : "Select a Raspberry",
                "select" : "Select",
                "download" : "Download the logs",
                "users" : "Users",
                "create_user" : "Create a user",
                "name_user" : "Username",
                "password" : "Password",
                "choix_role" : "Select a role",
                "connexion" : "Login",
                "create" : "Create the user",
                "admin" : "Administrator",
                "recherche" : "Search for a user",
                "recherche_user" : "Desired user",
                "search" : "Search",
                "result" : "Result",
                "name" : "Name",
                "supp" : "Delete",
                "confirm" : "Confirm",
                "cancel" : "Cancel"
            }
        }
    
    def tradCommercial(self):
        return {
            "fr" : {
                "user" : "Utilisateur",
                "logout" : "Déconnexion",
                "role" : "Rôle",
                "save_planning" : "Sauvegarder le planning",
                "ajout_music" : "Ajouter une musique",
                "heure_début" : "Heure de début",
                "titre" : "Titre",
                "artist" : "Artiste",
                "duree" : "Durée",
                "ajout" : "Ajouter",
                "supp" : "Supprimer"

            },

            "en" : {
                "user" : "User",
                "logout" : "Logout",
                "role" : "Role",
                "save_planning" : "Save the schedule",
                "ajout_music" : "Add music",
                "heure_début" : "Start time",
                "titre" : "Title",
                "artist" : "Artist",
                "duree" : "Duration",
                "ajout" : "Add",
                "supp" : "Delete"
            }
        }
    
    def tradMarketing(self):
        return {
            'fr': {
                "user" : "Utilisateur",
                "logout" : "Déconnexion",
                "play" : "Jouer playlist",
                "shuffle" : "Lecture aléatoire",
                "titre" : "Titre",
                "genre" : "Genre",
                "date" : "Date",
                "auteur" : "Artiste",
                "h3" : "Glisser-déposer ou cliquez pour sélectionner un fichier",
                "h3_1" : "Créer une nouvelle playlist",
                "nom" : "Nom de la playlist",
                "creer" : "Créer",
                "select" : "Choisir une playlist",
                "select_value" : "— Sélectionner —",
                "upload" : "Veuillez sélectionner une playlist",
                "submit" : "Envoyer",
                "convertir" : "Besoin de convertir en mp3?",
                "supp" : "Supprimer la playlist"
            },
            'en': {
                "user" : "User",
                "logout" : "Logout",
                "play" : "Play playlist",
                "shuffle" : "Shuffle playlist",
                "titre" : "Title",
                "genre" : "Genre",
                "date" : "Date",
                "auteur" : "Artist",
                "h3" : "Drag and drop or click to select a file",
                "h3_1" : "Create a new playlist",
                "nom" : "Playlist name",
                "creer" : "Create",
                "select" : "Select a playlist",
                "select_value" : "— Select —",
                "upload" : "Select a playlist",
                "submit" : "Send",
                "convertir" : "Need to convert to mp3?",
                "supp" : "Delete the playlist"
            }
        }