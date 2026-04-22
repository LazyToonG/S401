# Documentation des DAOs — Couche d'accès aux données

Ce document décrit les classes DAO (*Data Access Object*) du projet, qui gèrent toutes les interactions avec la base de données SQLite.

---

## Sommaire

- [UserDAOInterface](#userdaointerface)
- [UserDAO](#userdao--usersqlitedao)
- [MusicDAO](#musicdao)
- [PlaylistDAO](#playlistdao--playlistedao)
- [RaspberryDAO](#raspberrydao--raspberrysqlitedao)
- [ScheduleDAO](#scheduledao)
- [LogsDAO](#logsdao)
- [Structure de la base de données](#structure-de-la-base-de-données)

---

## UserDAOInterface

**Fichier :** `UserDAOInterface.py`

Interface (classe abstraite) définissant le contrat que tout DAO utilisateur doit respecter. Permet de découpler l'implémentation concrète du reste de l'application.

### Méthodes

| Méthode | Paramètres | Description |
|---|---|---|
| `createUser` | `username`, `password`, `role='commercial'` | Crée un nouvel utilisateur |
| `findByUsername` | `username` | Recherche un utilisateur par son nom |
| `verifyUser` | `username`, `password` | Vérifie les identifiants de connexion |
| `findAll` | — | Retourne tous les utilisateurs |
| `deleteByUsername` | `username` | Supprime un utilisateur par son nom |

---

## UserDAO — `UserSqliteDAO`

**Fichier :** `UserDAO.py`  
**Hérite de :** `UserDAOInterface`

Implémentation SQLite de la gestion des utilisateurs. Les mots de passe sont hashés avec **bcrypt**.

### Initialisation

```python
dao = UserSqliteDAO()
```

À l'initialisation, la table `users` est créée si elle n'existe pas, et un utilisateur `admin` (mot de passe : `admin`, rôle : `admin`) est automatiquement inséré lors de la première création.

### Table SQLite : `users`

| Colonne | Type | Description |
|---|---|---|
| `id` | INTEGER PK AUTOINCREMENT | Identifiant unique |
| `username` | TEXT UNIQUE | Nom d'utilisateur |
| `password` | TEXT | Mot de passe hashé (bcrypt) |
| `role` | TEXT | Rôle de l'utilisateur |

### Méthodes

| Méthode | Retour | Description |
|---|---|---|
| `createUser(username, password, role)` | `bool` | Crée un utilisateur avec mot de passe hashé |
| `findByUsername(username)` | `User \| None` | Trouve un utilisateur par son nom |
| `verifyUser(username, password)` | `User \| None` | Authentifie un utilisateur |
| `findAll()` | `list[User]` | Retourne tous les utilisateurs |
| `deleteByUsername(username)` | `bool` | Supprime un utilisateur |

---

## MusicDAO

**Fichier :** `MusicDAO.py`

Gère les musiques disponibles dans l'application.

### Initialisation

```python
dao = MusicDAO()
```

### Table SQLite : `music`

| Colonne | Type | Description |
|---|---|---|
| `id` | INTEGER PK AUTOINCREMENT | Identifiant unique |
| `title` | TEXT | Titre de la musique |
| `duration` | INTEGER | Durée en secondes |
| `path` | TEXT | Chemin vers le fichier audio |

### Méthodes

| Méthode | Retour | Description |
|---|---|---|
| `get_all()` | `list[Music]` | Retourne toutes les musiques |
| `get_by_id(music_id)` | `Music \| None` | Trouve une musique par son ID |
| `create(title, path, duration)` | `Music` | Ajoute une nouvelle musique |
| `delete(music_id)` | — | Supprime une musique |
| `get_musiques(order_by="title")` | `list[Music]` | Retourne les musiques triées (`"title"` ou `"duration"`) |

---

## PlaylistDAO — `PlaylisteDAO`

**Fichier :** `PlaylistDAO.py`

Gère les playlists. Les IDs des musiques sont stockés dans un champ texte séparé par des `|`.

### Initialisation

```python
dao = PlaylisteDAO()
```

À l'initialisation, la table `playlist` est créée si elle n'existe pas, et une playlist `annonces` par défaut est insérée automatiquement.

### Table SQLite : `playlist`

| Colonne | Type | Description |
|---|---|---|
| `id` | INTEGER PK AUTOINCREMENT | Identifiant unique |
| `title` | TEXT | Nom de la playlist |
| `music_ids` | TEXT | IDs des musiques séparés par `\|` (ex: `"1\|3\|7"`) |

### Méthodes

| Méthode | Retour | Description |
|---|---|---|
| `insert(playlist)` | — | Insère ou met à jour une playlist (`Playliste`) |
| `get(playlist_id)` | `Playliste \| None` | Retourne une playlist par son ID |
| `get_all()` | `list[Playliste]` | Retourne toutes les playlists |
| `delete(playlist_id)` | — | Supprime une playlist (à appeler après suppression des musiques associées) |

### Méthodes internes

- `_ids_to_str(ids)` : convertit une liste d'IDs en chaîne `"1|2|3"`
- `_str_to_ids(data)` : convertit une chaîne `"1|2|3"` en liste d'entiers

---

## RaspberryDAO — `RaspberrySqliteDAO`

**Fichier :** `RaspberryDAO.py`

Gère les Raspberry Pi enregistrés dans le système.

### Initialisation

```python
dao = RaspberrySqliteDAO()
```

### Table SQLite : `raspberry`

| Colonne | Type | Description |
|---|---|---|
| `idRasp` | INTEGER PK AUTOINCREMENT | Identifiant unique |
| `nom` | TEXT | Nom du Raspberry Pi |
| `ipRasp` | TEXT | Adresse IP du Raspberry Pi |

### Méthodes

| Méthode | Retour | Description |
|---|---|---|
| `findAll()` | `list[Raspberry]` | Retourne tous les Raspberry Pi |
| `createRasp(nom, ipRasp)` | `bool` | Enregistre un nouveau Raspberry Pi |
| `deleteRasp(idRasp)` | `bool` | Supprime un Raspberry Pi |
| `findByIp(idRasp)` | `str \| None` | Retourne l'adresse IP d'un Raspberry Pi par son ID |
| `findByNom(idRasp)` | `str \| None` | Retourne le nom d'un Raspberry Pi par son ID |

> **Note :** `findByIp` et `findByNom` recherchent par `idRasp` (identifiant), malgré leur nom.

---

## ScheduleDAO

**Fichier :** `ScheduleDAO.py`

Gère la planification hebdomadaire (jours, horaires de démarrage et éléments programmés).

### Initialisation

```python
dao = ScheduleDAO()
dao.init_db()  # À appeler explicitement pour créer les tables
```

À l'initialisation, les 7 jours de la semaine sont insérés avec une heure de départ par défaut à `"00:00"`.

### Tables SQLite

**`schedule_day`**

| Colonne | Type | Description |
|---|---|---|
| `day_name` | TEXT PK | Nom du jour (`monday`, `tuesday`, etc.) |
| `start_time` | TEXT | Heure de démarrage du programme (`HH:MM`) |

**`schedule_item`**

| Colonne | Type | Description |
|---|---|---|
| `id` | INTEGER PK AUTOINCREMENT | Identifiant unique |
| `day_name` | TEXT FK | Jour associé |
| `position` | INTEGER | Ordre dans le programme |
| `title` | TEXT | Titre de l'élément |
| `artist` | TEXT | Artiste |
| `duration` | INTEGER | Durée en secondes |
| `path` | TEXT | Chemin du fichier |

### Méthodes

| Méthode | Retour | Description |
|---|---|---|
| `init_db()` | — | Crée les tables et initialise les 7 jours |
| `get_start_time(day)` | `str` | Retourne l'heure de départ d'un jour |
| `update_start_time(day, start_time)` | — | Met à jour l'heure de départ d'un jour |
| `get_items_by_day(day)` | `list[Row]` | Retourne les éléments planifiés pour un jour, triés par position |
| `clear_day_items(day)` | — | Supprime tous les éléments d'un jour |
| `add_item(day, position, title, artist, duration, path)` | — | Ajoute un élément au programme d'un jour |

---

## LogsDAO

**Fichier :** `LogsDAO.py`

Gère les logs d'activité des Raspberry Pi. Contrairement aux autres DAOs, il est **indépendant de l'application Flask** et prend le chemin de la base de données en paramètre.

### Initialisation

```python
dao = LogsDAO(db_path="chemin/vers/database.db")
```

### Modèle : `Logs`

```python
Logs(id, idRaspberry, date, path)
```

### Table SQLite : `logs`

| Colonne | Type | Description |
|---|---|---|
| `id` | INTEGER PK AUTOINCREMENT | Identifiant unique |
| `idRaspberry` | TEXT | Identifiant du Raspberry Pi source |
| `date` | TEXT | Horodatage au format `YYYY-MM-DD HH:MM:SS` |
| `path` | TEXT | Chemin ou référence associée au log |

### Méthodes

| Méthode | Retour | Description |
|---|---|---|
| `get_all()` | `list[Logs]` | Retourne tous les logs triés par date croissante |
| `get_by_id(id)` | `Logs \| None` | Retourne un log par son ID |
| `get_by_raspberry(id_rasp)` | `list[Logs]` | Retourne les logs d'un Raspberry Pi |
| `get_by_date(date_str)` | `list[Logs]` | Retourne les logs d'une date donnée (format `YYYY-MM-DD`) |
| `get_latest()` | `Logs \| None` | Retourne le log le plus récent |
| `insert(idRaspberry, path, date=None)` | `int` | Insère un log (date = maintenant si non fournie), retourne l'ID |

---

## Structure de la base de données

```
database.db
├── users           (gestion des comptes)
├── music           (catalogue audio)
├── playlist        (playlists)
├── raspberry       (Raspberry Pi enregistrés)
├── schedule_day    (jours de la semaine + horaires)
├── schedule_item   (éléments planifiés)
└── logs            (historique d'activité)
```

---

> **Dépendances :** `sqlite3`, `bcrypt`, `Flask` (via `app`), `os`