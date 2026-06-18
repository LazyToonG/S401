from flask import session, request
class Traductionservice():

    def getLangue(self):
        langue_choisie = session.get('lang', 'fr')
        return langue_choisie
    
    def message_langue(self, message_fr, message_en):
        langue_choisie=Traductionservice.getLangue(self)
        if langue_choisie=='fr':
            message = message_fr
        elif langue_choisie=="en":
            message=message_en
        return message
    

    def tradNav(self):
        return {
            'fr': {
                "profil" : "Profil",
                "settings" : "Paramètres",
                "logout" : "Se déconnecter",
                "admin" : "Administrateur",
                "marketing" : "Marketing",
                "commercial" : "Commercial"
            },
            'en': {
                "profil" : "Profile",
                "settings" : "Settings",
                "logout" : "Log out",
                "admin" : "Administrator",
                "marketing" : "Marketing",
                "commercial" : "Commercial"
            }
        }

    def tradIndex(self):
        return {
            'fr': {
                "login" : "Se connecter",
                "signin" : "S'inscrire",
                'titre': "Bienvenue sur Musi-quali, votre plateforme de diffusion sonore",
                'desc_1': "Musi-quali est une plateforme qui vous permettra de diffuser de la musique et des messages sonores dans votre établissement. Vous pouvez préparer à l'avance un planning de musiques et de messages de publicité directement en ligne, faire des annonces quand vous voulez, et notre plateforme marche même en cas de coupure de connexion.",
                'desc_2': "Besoin d'une ambiance sonore dans votre magasin ? Utilisez Musi-quali !",
                'equipe_intro': "Nous somme une équipe d'éudiants en deuxième année en BUT Informatique à l'Universitée Sorbonne Paris Nord.",
                'equipe_liste': "Notre équipe est composée de :"
            },
            'en': {
                "login" : "Log in",
                "signin" : "Sign in",
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
                "signin" : "S'inscrire",
                "retour" : "Retour à l'accueil",
                "login" : "Se connecter",
                "user" : "Nom d'utilisateur",
                "password" : "Mot de passe",
                "login" : "Connexion",
                "mdp_oubli" : "Mot de passe oublié ?",
                "logout" : "Déconnexion",

                "commercial" : "Commercial",
                "marketing" : "Marketing",
                "admin" : "Administrateur",

                "error" : "Identifiants non valides"
            },

            "en" : {
                "signin" : "Sign in",
                "retour" : "Back to the home page",
                "login" : "Log in",
                "user" : "Username",
                "password" : "Password",
                "login" : "Login",
                "mdp_oubli" : "Forgotten your password?",
                "logout" : "Logout",

                "commercial" : "Commercial",
                "marketing" : "Marketing",
                "admin" : "Administrator",

                "error" : "Invalid Credentials"
            }
        }
    
    def tradSignin(self):
        return {
            "fr" : {
                "login" : "Se connecter",
                "retour" : "Retour à l'accueil",
                "signin" : "S'inscrire",
                "user" : "Nom d'utilisateur",
                "password" : "Mot de passe",
                "role" : "Rôle",
                "mail" : "Adresse Email",
                "confirm" : "Confirmer le mot de passe",
                "commercial" : "Commercial",
                "marketing" : "Marketing"
            },

            "en" : {
                "login" : "Log in",
                "retour" : "Back to the home page",
                "signin" : "Sign in",
                "user" : "Username",
                "role" : "Role",
                "password" : "Password",
                "mail" : "Email address",
                "confirm" : "Confirm password",
                "commercial" : "Commercial",
                "marketing" : "Marketing"
            }
        }

    def tradPassword(self):
        return {
            "fr" : {
                "new_mdp" : "Nouveau mot de passe",
                "signin" : "S'inscrire'",
                "retour" : "Retour à l'accueil",
                "saisir" : "Saisissez votre nouveau mot de passe",
                "confirm" : "Confirmer le mot de passe",
                "maj" : "Mettre à jour le mot de passe"
            },

            "en" : {
                "new_mdp" : "New password",
                "signin" : "Sign in",
                "retour" : "Back to the home page",
                "confirm" : "Confirm password",
                "maj" : "Update password"
            }
        }
    
    def tradAdmin(self):
        return {
            "fr" : {
                "profil" : "Profil",
                "settings" : "Paramètres",
                "logout" : "Se déconnecter",
                "admin" : "Administrateur",
                "marketing" : "Marketing",
                "commercial" : "Commercial",

                "gestion_rasp" : "Gestion des Raspberry",
                "terminal" : "Terminal",
                "gestion_user" : "Gestion des utilisateurs",
                "requetes" : "Requêtes administrateur",
                "recherche" : "Recherche",
                "supp_filtres" : "Enlever les filtres",
                "trier" : "Trier",
                "a_z" : "De A-Z",
                "z_a" : "De Z-A",
                "ip" : "Par IP",
                "supp_select" : "Supprimer la sélection",
                "tri_role" : "Par rôle",
                "create_user" : "Créer un utilisateur",
                "name_user" : "Nom d'utilisateur",
                "nom" : "Nom",
                "mail" : "E-mail",
                "password" : "Mot de passe",
                "role" : "Rôle",
                "etat" : "État",
                "connexion" : "Connexion",
                "commercial" : "Commercial",
                "marketing" : "Marketing",
                "admin" : "Administrateur",
                "modif" : "Modifier",
                "enregistrer"  : "Enregistrer",
                "cancel" : "Annuler",
                "confirm_supp"  : "Confirmer la suppression",
                "confirm_q" : "Voulez-vous vraiment supprimer l'utilisateur ",
                "confirm" : "Confirmer",
                "titreRasp" : "Ajouter une Raspberry",
                "nomRasp" : "Quel est l'identifiant/nom de la nouvelle Raspberry que vous voulez insérer ?",
                "ipRasp" : "Quel est l'adresse IP de la nouvelle Raspberry que vous voulez insérer ?",
                "mdpRasp" : "Quel est le mot de passe de cette Raspberry ?",
                "form_nomRasp" : "Entrez l'identifiant de la Raspberry",
                "form_ipRasp" : "Entrez l'adresse IP de la Raspberry",
                "form_mdpRasp" : "Entrez le mot de passe de la Raspberry",
                "bouton_ajoutRasp" : "Ajouter la Raspberry",
                "aucun_rasp" : "Aucune Raspberry trouvée.",
                "aucun_user" : "Aucun utilisateur trouvé.",



                "fichier" : "Envoyer des fichiers musiques manuellement",
                "user" : "Utilisateur",
                "logout" : "Déconnexion",
                "select_rasp" : "Sélectionner une Raspberry",
                "select" : "Sélectionner",
                "download" : "Télécharger les logs",
                "users" : "Utilisateurs",
                
                "connexion" : "Connexion",
                "recherche_user" : "Utilisateur recherché",
                "search" : "Rechercher",
                "result" : "Résultat",
                "name" : "Nom",
                "supp" : "Supprimer",
                
            },

            "en" : {"profil" : "Profile",
                "settings" : "Settings",
                "logout" : "Log out",
                "admin" : "Administrator",
                "marketing" : "Marketing",
                "commercial" : "Commercial",

                "gestion_rasp" : "Raspberry Management",
                "terminal" : "Terminal",
                "gestion_user" : "User management",
                "requetes" : "Administrator requests",
                "recherche" : "Search",
                "supp_filtres" : "Remove the filters",
                "trier" : "Sort",
                "a_z" : "From A to Z",
                "z_a" : "From Z to A",
                "ip" : "By IP",
                "supp_select" : "Clear selection",
                "tri_role" : "By role",
                "name_user" : "Username",
                "nom" : "Name",
                "mail" : "Email",
                "password" : "Password",
                "role" : "Role",
                "etat" : "Status",
                "connexion" : "Log in",
                "create" : "Create a user",
                "commercial" : "Commercial",
                "marketing" : "Marketing",
                "admin" : "Administrator",
                "modif" : "Edit",
                "enregistrer"  : "Save",
                "cancel" : "Cancel",
                "confirm_supp"  : "Confirm deletion",
                "confirm_q" : "Are you sure you want to delete this user ",
                "confirm" : "Confirm",
                "titreRasp" : "Add a Raspberry",
                "nomRasp" : "What is the identifier/name of the new Raspberry you want to insert?",
                "ipRasp" : "What is the IP address of the new Raspberry you want to insert?",
                "mdpRasp" : "What is the password for this Raspberry ?",
                "form_nomRasp" : "Enter the Raspberry identifier",
                "form_ipRasp" : "Enter the Raspberry IP address",
                "form_mdpRasp" : "Enter the Raspberry password",
                "bouton_ajoutRasp" : "Add the Raspberry",
                "aucun_rasp" : "No Raspberry found.",
                "aucun_user" : "No users found.",



                "fichier" : "Manually send music files",
                "user" : "User",
                "logout" : "Logout",
                "select_rasp" : "Select a Raspberry",
                "select" : "Select",
                "download" : "Download the logs",
                "users" : "Users",
                "create_user" : "Create a user",
                "name_user" : "Username",
                "password" : "Password",
                "choix_role" : "Select a role",
                "connexion" : "Login",
                
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
                "profil" : "Profil",
                "settings" : "Paramètres",
                "logout" : "Se déconnecter",
                "admin" : "Administrateur",
                "marketing" : "Marketing",
                "commercial" : "Commercial",

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
                "profil" : "Profile",
                "settings" : "Settings",
                "logout" : "Log out",
                "admin" : "Administrator",
                "marketing" : "Marketing",
                "commercial" : "Commercial",

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
                "profil" : "Profil",
                "settings" : "Paramètres",
                "logout" : "Se déconnecter",
                "admin" : "Administrateur",
                "marketing" : "Marketing",
                "commercial" : "Commercial",

                "playlist" : "Playlists",
                "musics" : "Toutes les musiques",
                "ajout_play" : "Créer une nouvelle playlist",
                "duree" : "Durée :",
                "h3" : "Glisser-déposer ou cliquez pour sélectionner un fichier",
                "ajout_bd" : "Ajouter à la base de données",
                "convertir" : "Convertir en MP3",


                "user" : "Utilisateur",
                "logout" : "Déconnexion",
                "play" : "Jouer playlist",
                "shuffle" : "Lecture aléatoire",
                "nom" : "Nom de la playlist",
                "creer" : "Créer",
                "select" : "Choisir une playlist",
                "select_value" : "— Sélectionner —",
                "upload" : "Veuillez sélectionner une playlist",
                "submit" : "Envoyer",
                "supp" : "Supprimer la playlist"
            },

            'en': {
                "profil" : "Profile",
                "settings" : "Settings",
                "logout" : "Log out",
                "admin" : "Administrator",
                "marketing" : "Marketing",
                "commercial" : "Commercial",

                "playlist" : "Playlists",
                "musics" : "All the music",
                "ajout_play" : "Create a new playlist",
                "duree" : "Duration:",
                "h3" : "Drag and drop or click to select a file",
                "ajout_bd" : "Add to the database",
                "convertir" : "Convert to MP3",

                "user" : "User",
                "logout" : "Logout",
                "play" : "Play playlist",
                "shuffle" : "Shuffle playlist",
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
    

    def tradProfil(self):
        return {
            "fr" : {
                "profil" : "Profil",
                "settings" : "Paramètres",
                "logout" : "Se déconnecter",
                "admin" : "Administrateur",
                "marketing" : "Marketing",
                "commercial" : "Commercial",

                "profile" : "Mon Profil",
                "infos" : "Gérez vos informations personnelles",
                "name_user" : "Nom d'utilisateur",
                "mail" : "E-mail",
                "role" : "Rôle",
                "modif_mdp" : "Modifier le mot de passe",
                "modif_info" : "Modifier les infos",
                "enregistrer"  : "Enregistrer",
                "cancel" : "Annuler",
                "ancien_mdp" : "Ancien mot de passe",
                "new_mdp" : "Nouveau mot de passe",
                "confirm_mdp" : "Confirmer le nouveau mot de passe"

            },

            "en" : {
                "profil" : "Profile",
                "settings" : "Settings",
                "logout" : "Log out",
                "admin" : "Administrator",
                "marketing" : "Marketing",
                "commercial" : "Commercial",

                "profile" : "My Profile",
                "infos" : "Manage your personal information",
                "name_user" : "Username",
                "mail" : "Email",
                "role" : "Role",
                "modif_mdp" : "Change password",
                "modif_info" : "Edit details",
                "enregistrer"  : "Save",
                "cancel" : "Cancel",
                "ancien_mdp" : "Old password",
                "new_mdp" : "New password",
                "confirm_mdp" : "Confirm the new password"
                
            }
        }
    

    def tradSettings(self):
        return {
            "fr" : {
                "profil" : "Profil",
                "settings" : "Paramètres",
                "logout" : "Se déconnecter",
                "admin" : "Administrateur",
                "marketing" : "Marketing",
                "commercial" : "Commercial",

                "settings" : "Préférences de l'application",
                "langue" : "Langue de l'interface",
                "affichage" : "Affichage",
                "mode" : "Activer le Mode Sombre",
                "enregistrer"  : "Enregistrer les modifications"
                

            },

            "en" : {
                "profil" : "Profile",
                "settings" : "Settings",
                "logout" : "Log out",
                "admin" : "Administrator",
                "marketing" : "Marketing",
                "commercial" : "Commercial",

                "settings" : "App settings",
                "langue" : "Interface language",
                "affichage" : "Display",
                "mode" : "Enable Dark Mode",
                "enregistrer"  : "Save changes"
                
            }
        }
    
    def tradEntreprise(self):
        return {
            "fr" : {
                "tousEntreprise" : "Liste des entreprises"
            },
            "eng" : {
                "tousEntreprise" : "List of all the companys"
            }}