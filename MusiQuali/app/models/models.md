# Documentation des Modèles & Configuration BDD

Ce document décrit les classes métier (modèles) et la configuration de la base de données du projet.

---

## Sommaire

- [Configuration BDD — db.py](#configuration-bdd--dbpy)
- [User](#user)
- [Music](#music)
- [Musique](#musique)
- [Playliste](#playliste)
- [Raspberry](#raspberry)
- [Schedule](#schedule)
- [Logs](#logs)
- [Note sur la duplication Music / Musique](#note-sur-la-duplication-music--musique)

---

## Configuration BDD — `db.py`

**Fichier :** `db.py`

Fournit deux fonctions utilitaires pour la connexion et l'initialisation de la base de données SQLite partagée (`database.db`).

### Fonctions

#### `get_db() → Connection`

Ouvre et retourne une connexion SQLite avec `row_factory = sqlite3.Row` (accès aux colonnes par nom).

```python
conn = get_db()
```

#### `init_db()`

Crée les tables si elles n'existent pas et insère les 7 jours de la semaine avec une heure de départ par défaut à `"08:00"`.

**Tables créées :**

| Table | Description |
|---|---|
| `playlists` | Playlists (id, name) |
| `musics` | Musiques liées à une playlist (id, title, artist, duration, path, playlist_id) |
| `schedule_days` | Jours de la semaine avec heure de départ (day_name, start_time) |
| `schedule_items` | Éléments planifiés par jour (id, day_name, position, title, artist, duration, path) |

> **Note :** Ces tables (`playlists`, `musics`) coexistent avec les tables `playlist` et `music` définies dans les DAOs. Vérifier quelle version est effectivement utilisée.

---

## User

**Fichier :** `User.py`

Représente un utilisateur authentifié de l'application.

### Constructeur

```python
User(dico: dict)
```

Prend un dictionnaire (typiquement une ligne SQLite convertie en `dict`).

### Attributs

| Attribut | Type | Description |
|---|---|---|
| `id` | int | Identifiant unique |
| `username` | str | Nom d'utilisateur |
| `role` | str | Rôle (`admin`, `commercial`, `marketing`) |

### Exemple

```python
user = User({"id": 1, "username": "alice", "role": "admin"})
```

---

## Music

**Fichier :** `Music.py`

Représente une musique dans le catalogue (version anglophone, utilisée par `MusicDAO`).

### Constructeur

```python
Music(id, title, path, duration)
```

### Attributs

| Attribut | Type | Description |
|---|---|---|
| `id` | int | Identifiant unique |
| `title` | str | Titre de la musique |
| `path` | str | Chemin vers le fichier audio |
| `duration` | int | Durée en secondes |
| `artist` | str | Artiste (vide par défaut `""`) |

### Propriétés (alias pour les templates)

| Propriété | Retourne | Description |
|---|---|---|
| `titre` | `self.title` | Alias français pour les templates |
| `artiste` | `self.artist` | Alias français pour les templates |

---

## Musique

**Fichier :** `Musique.py`

Représente une musique dans le catalogue (version francophone, utilisée par `MusiqueService`).

### Constructeur

```python
Musique(id, titre, chemin, longueure)
```

### Attributs

| Attribut | Type | Description |
|---|---|---|
| `id` | int | Identifiant unique |
| `titre` | str | Titre de la musique |
| `chemin` | str | Chemin vers le fichier audio |
| `longueure` | int | Durée en secondes |

---

## Playliste

**Fichier :** `Playliste.py`

Représente une playlist contenant une liste de musiques (référencées par leurs IDs).

### Constructeur

```python
Playliste(title, id=None, music_ids=None)
```

### Attributs

| Attribut | Type | Description |
|---|---|---|
| `id` | int \| None | Identifiant (None avant insertion en BDD) |
| `title` | str | Nom de la playlist |
| `music_ids` | list[int] | Liste des IDs des musiques (`[]` par défaut) |

### Méthodes

#### `addMusique(music_id: int)`

Ajoute un ID de musique à la liste `music_ids`.

```python
playlist.addMusique(42)
```

> Les IDs sont sérialisés en `"id1|id2|id3"` par le `PlaylisteDAO` pour le stockage en base.

---

## Raspberry

**Fichier :** `Raspberry.py`

Représente un Raspberry Pi enregistré dans le système.

### Constructeur

```python
Raspberry(idRasp, nom, ipRasp)
```

### Attributs

| Attribut | Type | Description |
|---|---|---|
| `idRasp` | int | Identifiant unique |
| `nom` | str | Nom d'utilisateur SSH du Raspberry Pi |
| `ipRasp` | str | Adresse IP du Raspberry Pi |

---

## Schedule

**Fichier :** `Scheduler.py`

Représente le planning hebdomadaire complet. Chaque jour est une liste dont le premier élément est l'heure de départ (`"HH:MM"`) et les suivants sont des objets musique.

### Constructeur

```python
Schedule(planning: dict)
```

Le dictionnaire `planning` doit contenir les clés `start_time`, `Monday`, `Tuesday`, ..., `Sunday`.

### Attributs

| Attribut | Type | Description |
|---|---|---|
| `start_time` | str | Heure de départ globale (`"HH:MM"`) |
| `monday` … `sunday` | list | Liste `[start_time, music1, music2, ...]` pour chaque jour |

### Méthodes

#### `add_task(day, music, index) → bool`

Ajoute une musique à un jour à la position `index`. Retourne `False` si la durée totale du jour dépasse 86 400 secondes (24h).

```python
ok = schedule.add_task("monday", music_obj, 0)
```

#### `move_task(from_day, from_idx, to_day, to_idx)`

Déplace une musique d'un jour et d'une position vers un autre jour et une autre position.

```python
schedule.move_task("monday", 0, "tuesday", 1)
```

#### `get_day_data(day_name) → dict`

Calcule les horaires de passage pour chaque musique d'un jour, à partir de l'heure de départ.

**Retourne :**

```python
{
    "start_offset_min": int,   # heure de départ en minutes depuis minuit
    "musics": [
        {
            "obj": music_obj,
            "time": "HH:MM",   # heure de passage calculée
            "start_sec": int,  # seconde de départ
            "duration": int    # durée en secondes
        },
        ...
    ]
}
```

#### `update_day(day, musics, start_time=None)`

Remplace entièrement la liste de musiques d'un jour. Si `start_time` n'est pas fourni, conserve l'heure de départ existante.

```python
schedule.update_day("monday", [music1, music2], start_time="09:00")
```

---

## Logs

**Fichier :** `Logs.py`

Représente une entrée de log d'activité d'un Raspberry Pi.

### Constructeur

```python
Logs(id, idRaspberry, date, path)
```

### Attributs

| Attribut | Type | Description |
|---|---|---|
| `id` | int | Identifiant unique |
| `idRaspberry` | str | Identifiant du Raspberry Pi source |
| `date` | str | Horodatage au format `YYYY-MM-DD HH:MM:SS` |
| `path` | str | Chemin ou référence associée au log |

---

## Note sur la duplication Music / Musique

Le projet contient deux classes représentant une musique :

| Classe | Fichier | Utilisée par | Langue des attributs |
|---|---|---|---|
| `Music` | `Music.py` | `MusicDAO` | Anglais (`title`, `path`, `duration`) |
| `Musique` | `Musique.py` | `MusiqueService` | Français (`titre`, `chemin`, `longueure`) |

La classe `Music` ajoute des propriétés `titre` et `artiste` pour assurer la compatibilité avec les templates qui utilisent la convention francophone. À terme, une harmonisation des deux classes serait souhaitable.