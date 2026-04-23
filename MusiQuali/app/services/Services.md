# Documentation des objets services et de la logique metier

Ce documentdécrit les classes Service et leur logique metier.

---

# Sommaire

- [__init__.py](#__init__py)
- [MusiqueService.py](#musiqueservice)
- [playlistServiceMarketing.py](#playlistservicemarketing)
- [RaspberryService.py](#raspberryservicepy)
- [service_playlist.py](#service_playlistpy)
- [service_schedule.py](#service_schedulepy)
- [TraductionService.py](#traductionservicepy)
- [UserService.py](#userservicepy)

---

## <a name="__init__.py"></a>__init__.py

[Fichier](__init__.py)

Fichier d'initialisation



## <a name="musiqueservice"></a>MusiqueService

[Fichier](MusiqueService.py)

MusiqueService gere les fichiers MP3 et métadonnées en base de données.

# Fonctionnalités
Téléchargement : Enregistre les MP3 dans static/rasdata/allMusic, extrait durée avec mutagen, et stocke les infos via MusicDAO.
Récupération : get_musiques(sort) liste les musiques (tri possible par title ou autre champ).
Suppression : delete_musique(music) supprime l'entrée en base de données et le fichier physique.
Vérification : allowed_file(filename) autorise uniquement les fichiers .mp3.

# Dépendances:
MusicDAO pour les opérations en base de données.
mutagen pour lire la durée des MP3.
secure_filename pour sécuriser les noms de fichiers.


## <a name="playlistservicemarketing"></a>playlistServiceMarketing

[Fichier](playlistServiceMarketing)

PlaylistService gère les playlists et et leurs les musiques.

# Fonctionnalités

Création : create_playlist(title) crée une nouvelle playlist en base de données.
Récupération : get_all() liste toutes les playlists, get_by_id(playlist_id) récupère une playlist par son ID.
Ajout de musique : add_music_to_playlist(playlist_id, music_id) ajoute une musique à une playlist (lève une erreur si la playlist n'existe pas).
Liste des musiques : musics_in_playlist(playlist_id) retourne la liste des objets Music associés à une playlist.
Suppression : delete_playlist(playlist_id) supprime une playlist de la base de données.

# Dépendances

PlaylisteDAO pour les opérations en base de données sur les playlists.
MusicDAO pour récupérer les objets Music associés.
Playliste (modèle) pour représenter une playlist.


## <a name="raspberryservicepy"></a>RaspberryService.py

RaspberryService gère les appareils Raspberry Pi et leurs interactions (synchronisation, commandes SSH, etc.).

# Fonctionnalités

Gestion des Raspberry Pi :

montreToutRasp() : Liste tous les Raspberry Pi enregistrés.
ajoutR(identifiant, ipRasp) : Ajoute un nouveau Raspberry Pi en base de données.
selectRIp(ipRasp) / selectRNom(nom) : Récupère un Raspberry Pi par son IP ou son nom.
supprimeR(ipRasp) : Supprime un Raspberry Pi de la base de données.
verifieShellRasp() : Vérifie l'état des connexions SSH.


Synchronisation et commandes :

envoieChaqueChangementPlanning() : Synchronise les fichiers locaux (./app/static/rasdata/) vers chaque Raspberry Pi via rsync et exécute un script Python (RAS.py) à distance.
pingTout() : Effectue un ping sur chaque Raspberry Pi pour vérifier leur disponibilité (utilisé pour les logs).


# Dépendances

RaspberrySqliteDAO pour les opérations en base de données.
subprocess pour exécuter des commandes shell (rsync, ssh, ping).
time pour gérer les délais d'attente.


## <a name="service_playlistpy"></a>service_playlist.py


le service que lucas a fait plutot que de se servir de celui que j'ai préparé.
le truc est redondant et a prêté à la confusion.
il a également fait son propre modèle et dao de musique.      >:(
le sien fait rien que je ne fais pas déja parceque j'ai pévu EXPRES que ca fasse ce dont il aurait besoin
je lui ai dit : sers toi des modeles et DAO que j'ai préparé et aménagé EXPRES
mais Noooooooooooooooooooooooooon, il sait mieux que tout le monde bien suuuuur

## <a name="service_schedulepy"></a>service_schedule.py

ScheduleService gère les plannings du marketing.

# Fonctionnalités

_load_planning() : charge les plannings depuis la bd et construit un objet Schedule avec les musiques organisées par jour.
get_planning() : retourne le planning complet sous forme d'objet Schedule. (vide jusqu'ici)
Synchronisation : sync_day(day, tasks, start_time) met à jour un jour le planning
export_planning() : exporte le planning au format JSON (fichier en mémoire).

# Dépendances

ScheduleDAO pour les opérations en base de données.
Scheduler et Music (modèles) pour représenter les plannings et les musiques.
json et io pour l'export des données.


## <a name="traductionservicepy"></a>TraductionService.py

# fonctionnalités
retourne les valeures françaises ou anglaises des textes selon la langue choisie


## <a name="userservicepy"></a>UserService.py

UserService gère les utilisateurs et leur authentification.

# Fonctionnalités

getUserByUsername(username) : Retourne un ou plusieurs utilisateurs correspondant au nom d'utilisateur.
getUsers() : Retourne la liste de tous les utilisateurs.

signin(username, password, role) : Crée un nouvel utilisateur.
login(username, password) : Vérifie les identifiants de l'utilisateur.

Suppression : deleteUser(username) : Supprime un utilisateur par son nom d'utilisateur.

# Dépendances :
UserSqliteDAO pour les opérations en base de données.
