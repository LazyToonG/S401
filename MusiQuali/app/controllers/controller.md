# Documentation des Controllers — Couche de présentation (Flask)

Ce document décrit les controllers Flask du projet, qui gèrent les routes HTTP et la logique de présentation.

---

## Sommaire

- [Authentification & Sécurité — LoginController](#logincontroller)
- [Page d'accueil — IndexController](#indexcontroller)
- [Administration — AdminController](#admincontroller)
- [Commercial / Planning — controllers_commercial](#controllers_commercial)
- [Marketing — MarketingController](#marketingcontroller)
- [Raspberry Pi — RaspberryController](#raspberrycontroller)
- [Système de rôles](#système-de-rôles)
- [Récapitulatif des routes](#récapitulatif-des-routes)

---

## LoginController

**Fichier :** `LoginController.py`  
**Dépendances :** `UserService`, `TraductionService`

Gère l'authentification des utilisateurs et fournit les décorateurs de sécurité utilisés dans tous les autres controllers.

### Décorateurs de sécurité

#### `@reqlogged`

Vérifie que l'utilisateur est connecté (clé `logged` présente en session). Redirige vers `/login` si ce n'est pas le cas.

```python
@reqlogged
def ma_route():
    ...
```

#### `@reqrole(*roles)`

Vérifie que l'utilisateur est connecté **et** qu'il possède l'un des rôles autorisés. Retourne une erreur `403` si le rôle est insuffisant.

```python
@reqrole("admin", "commercial")
def ma_route():
    ...
```

### Routes

#### `GET/POST /login`

Page de connexion. En `POST`, vérifie les identifiants via `UserService` et redirige selon le rôle :

| Rôle | Redirection |
|---|---|
| `admin` | `/admin` |
| `marketing` | `/marketing` |
| `commercial` | `/commercial` |
| autre | `/` |

#### `GET/POST /admin/create_user`

Formulaire de création d'un utilisateur. Rôle par défaut : `commercial`.

#### `GET /logout`

Déconnexion : vide la session et redirige vers `/login`.  
**Accès :** utilisateur connecté (`@reqlogged`)

---

## IndexController

**Fichier :** `IndexController.py`  
**Dépendances :** `TraductionService`

Controller minimal pour la page d'accueil publique.

### Routes

#### `GET /`

Affiche la page d'accueil (`index.html`) avec les traductions de la langue courante.

---

## AdminController

**Fichier :** `AdminController.py`  
**Dépendances :** `UserService`, `RaspberryService`, `TraductionService`  
**Accès :** rôle `admin` requis sur toutes les routes

Gère le tableau de bord administrateur et les opérations sur les comptes utilisateurs.

### Routes

#### `GET /admin`

Affiche le tableau de bord admin (`admin.html`) avec la liste des Raspberry Pi enregistrés.

#### `POST/GET /admin/create`

Crée un nouvel utilisateur. Vérifie que les champs sont remplis et que le nom d'utilisateur n'existe pas déjà.

**Données formulaire :**

| Champ | Description |
|---|---|
| `username` | Nom d'utilisateur |
| `password` | Mot de passe |
| `role` | Rôle (`admin`, `commercial`, `marketing`) |

#### `POST /admin/delete`

Supprime un utilisateur. Interdit la suppression du compte actuellement connecté. Un bouton `cancel` dans le formulaire annule l'opération.

**Données formulaire :**

| Champ | Description |
|---|---|
| `username` | Nom d'utilisateur à supprimer |
| `decision` | `"cancel"` pour annuler |

#### `POST/GET /admin/search`

Recherche un utilisateur par son nom et l'affiche dans le dashboard.

**Données formulaire :**

| Champ | Description |
|---|---|
| `username` | Nom d'utilisateur à rechercher |

---

## controllers_commercial

**Fichier :** `controllers_commercial.py`  
**Dépendances :** `RaspberryService`, `service_playlist`, `service_schedule`, `TraductionService`

Gère les fonctionnalités du planning hebdomadaire et les interactions avec les Raspberry Pi.

### Routes

#### `GET /commercial`

Affiche le planning (`planning.html`) avec les playlists disponibles.  
**Accès :** rôles `admin`, `commercial`

#### `GET /admin`

Affiche le tableau de bord admin avec la liste des playlists et des Raspberry Pi.  
**Accès :** rôle `admin`

> **Note :** Cette route entre en conflit avec celle définie dans `AdminController.py`. À harmoniser.

#### `POST /add_playlist`

Crée une nouvelle playlist à partir d'un nom de formulaire.

#### `GET /api/playlists`

Retourne la liste des playlists au format JSON.

#### `POST /move`

Déplace une musique d'un jour à un autre dans le planning.

**Corps JSON :**

```json
{
  "from_day": "monday",
  "from_index": 0,
  "to_day": "tuesday",
  "to_index": 2
}
```

#### `POST /sync_day`

Synchronise les tâches d'un jour entier avec l'heure de départ.

**Corps JSON :**

```json
{
  "day": "monday",
  "tasks": [...],
  "start_time": "08:00"
}
```

#### `POST /save_export`

Exporte le planning en JSON dans `static/rasdata/planning_export.json`, puis envoie le fichier à tous les Raspberry Pi via `RaspberryService`.

---

## MarketingController

**Fichier :** `MarketingController.py`  
**Dépendances :** `MusiqueService`, `PlaylistService`, `TraductionService`

Gère l'espace marketing : consultation et gestion des playlists et des musiques.

### Accès par rôle

| Rôle | Accès |
|---|---|
| `admin` | Toutes les playlists et fonctionnalités |
| `marketing` | Toutes les playlists et fonctionnalités |
| `commercial` | Uniquement la playlist `message` |

### Routes

#### `GET/POST /marketing`

Page principale marketing. Affiche les playlists et musiques disponibles.  
En `POST` avec un `playlist_id`, affiche les musiques contenues dans la playlist sélectionnée.  
**Accès :** rôles `admin`, `marketing`, `commercial`

#### `GET /delete/<int:id>`

Supprime une musique par son ID et redirige vers `/marketing`.

#### `GET /search_by_title`

Recherche une musique par titre via le paramètre `?title=`.

#### `POST /playlist/create`

Crée une nouvelle playlist.  
**Accès :** rôles `admin`, `marketing`

**Données formulaire :**

| Champ | Description |
|---|---|
| `title` | Nom de la playlist |

#### `POST /playlist/delete`

Supprime une playlist et toutes ses musiques associées.  
**Accès :** rôles `admin`, `marketing`

**Données formulaire :**

| Champ | Description |
|---|---|
| `playlist_id` | ID de la playlist à supprimer |

#### `POST /upload`

Upload un fichier audio et l'associe à une playlist.  
Les utilisateurs `commercial` ne peuvent uploader que dans la playlist `message`.

**Données formulaire :**

| Champ | Description |
|---|---|
| `audio` | Fichier audio |
| `playlist_id` | ID de la playlist cible |

---

## RaspberryController

**Fichier :** `RaspberryController.py`  
**Dépendances :** `RaspberryService`, `TraductionService`, `subprocess`, `ipaddress`  
**Accès :** rôle `admin` requis sur toutes les routes

Gère l'ajout, la suppression et les actions distantes sur les Raspberry Pi.

### Routes

#### `POST /admin/add_rasp`

Enregistre un nouveau Raspberry Pi après validation de l'adresse IP. Si l'IP est valide et non dupliquée, copie les fichiers initiaux via `scp`.

**Données formulaire :**

| Champ | Description |
|---|---|
| `ipRasp` | Adresse IP du Raspberry Pi |
| `nom` | Nom d'utilisateur SSH du Raspberry Pi |

#### `POST /admin/action_rasp`

Effectue une action sur un Raspberry Pi sélectionné.

**Données formulaire :**

| Champ | Description |
|---|---|
| `raspberry-select` | ID du Raspberry Pi ciblé |
| `action` | Action à effectuer (voir tableau ci-dessous) |

**Actions disponibles :**

| Valeur `action` | Description |
|---|---|
| `delete-rasp` | Supprime le Raspberry Pi de la base de données |
| `envoie-ping` | Envoie un ping (`-c 4`) pour vérifier la connectivité |
| `test` | Synchronise les fichiers via `rsync` puis exécute `RAS.py` à distance via `ssh` |

---

## Système de rôles

| Rôle | Accès |
|---|---|
| `admin` | Accès complet (dashboard, utilisateurs, Raspberry Pi, planning, marketing) |
| `marketing` | Gestion des playlists et musiques |
| `commercial` | Planning + playlist `message` uniquement |

La vérification des rôles est centralisée dans `LoginController.py` via le décorateur `@reqrole`.

---

## Récapitulatif des routes

| Méthode | Route | Controller | Rôle requis |
|---|---|---|---|
| `GET` | `/` | IndexController | — |
| `GET/POST` | `/login` | LoginController | — |
| `GET` | `/logout` | LoginController | connecté |
| `GET/POST` | `/admin/create_user` | LoginController | — |
| `GET` | `/admin` | AdminController | `admin` |
| `POST/GET` | `/admin/create` | AdminController | `admin` |
| `POST` | `/admin/delete` | AdminController | `admin` |
| `POST/GET` | `/admin/search` | AdminController | `admin` |
| `POST` | `/admin/add_rasp` | RaspberryController | `admin` |
| `POST` | `/admin/action_rasp` | RaspberryController | `admin` |
| `GET` | `/commercial` | controllers_commercial | `admin`, `commercial` |
| `POST` | `/move` | controllers_commercial | — |
| `POST` | `/sync_day` | controllers_commercial | — |
| `POST` | `/save_export` | controllers_commercial | — |
| `GET` | `/api/playlists` | controllers_commercial | — |
| `GET/POST` | `/marketing` | MarketingController | `admin`, `marketing`, `commercial` |
| `GET` | `/delete/<id>` | MarketingController | — |
| `GET` | `/search_by_title` | MarketingController | — |
| `POST` | `/playlist/create` | MarketingController | `admin`, `marketing` |
| `POST` | `/playlist/delete` | MarketingController | `admin`, `marketing` |
| `POST` | `/upload` | MarketingController | — |