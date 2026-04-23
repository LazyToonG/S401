# Documentation Front-end — Styles, Scripts & Assets

Ce document décrit les fichiers statiques du projet : feuilles de style CSS, scripts JavaScript et ressources graphiques.

---

## Sommaire

- [Logo](#logo)
- [Styles globaux — style.css](#styles-globaux--stylecss)
- [Page d'accueil — style_accueil.css](#page-daccueil--style_accueilcss)
- [Administration — admin.css](#administration--admincss)
- [Marketing — marketing.css](#marketing--marketingcss)
- [Planning — planning_style.css](#planning--planning_stylecss)
- [Alertes — message_alert.css & message_alert.js](#alertes--message_alertcss--message_alertjs)
- [Script global — script.js](#script-global--scriptjs)
- [Script planning — planning_script.js](#script-planning--planning_scriptjs)
- [Système de thèmes (clair / sombre)](#système-de-thèmes-clair--sombre)
- [Palette de couleurs](#palette-de-couleurs)

---

## Logo

**Fichier :** `logo.png`

Logo de l'application représentant un nœud papillon rouge avec un « M » central et des ondes sonores sur les côtés. Utilisé dans la navbar et en filigrane sur les pages principales (opacité 20%).

---

## Styles globaux — `style.css`

**Utilisé par :** toutes les pages internes (admin, marketing, planning, login…)

Définit la charte graphique de base de l'application : layout, navbar, boutons, mode sombre et typographie.

### Layout

Le `body` utilise un flexbox vertical (`flex-direction: column`) pour garantir que le pied de page reste en bas. Fond bleu clair `#b5d3f0`, police serif (Times New Roman).

Un filigrane du logo est positionné en absolu au centre de la page via `body::after`, avec une opacité de 0.2 et un `z-index: -1`.

### Navbar `.nav`

Flexbox horizontal avec justification `space-between`. Fond bleu `#267ac9`, texte blanc. Les éléments enfants ont un fond semi-transparent `#ffffff4c` avec bordures arrondies.

### Boutons

| Classe | Couleur | Usage |
|---|---|---|
| `.btn-rouge` | `#a33e3e` | Action destructive |
| `.btn-bleu` | `#267ac9` | Action principale |
| `.btn-logout` | Blanc / noir | Déconnexion (mode clair) |
| `.btn-logout-sombre` | Noir / blanc | Déconnexion (mode sombre) |
| `.seconnecte` | `#d02424` | Bouton de connexion sur la page d'accueil |

### Mode sombre

La classe `.sombre` applique fond `#083967` et texte blanc. Les `.card.sombre` utilisent `#1a2b3c` avec des inputs en `#0e1a25`.

---

## Page d'accueil — `style_accueil.css`

**Utilisé par :** `index.html`

Feuille de style dédiée à la page publique d'accueil, avec une mise en page plus légère que `style.css`.

### Spécificités

- `.h1` : conteneur centré en flexbox, hauteur `50vh`. Le filigrane du logo est appliqué via `::after` sur ce conteneur (et non sur le `body` comme dans `style.css`).
- `.presentation` et `.equipe` : blocs de contenu avec fond bleu `#267ac9`, texte blanc, bordures arrondies — utilisés pour présenter le projet et l'équipe.
- Les textes `<p>` et `<ul>` ont une taille de `20px`.

---

## Administration — `admin.css`

**Utilisé par :** `admin.html`

Styles spécifiques au tableau de bord administrateur.

### Layout

Grille CSS à deux colonnes (`2fr 1fr`) avec deux lignes. Le `.left-panel` occupe toute la hauteur (`grid-row: 1 / 3`).

```
┌─────────────────────┬──────────────┐
│                     │  top-right   │
│    left-panel       ├──────────────┤
│                     │  bot-right   │
└─────────────────────┴──────────────┘
```

### Composants notables

- **`.terminal-screen`** : zone noire (`#0d0d0d`) avec texte vert monospace (`#00ff88`), hauteur fixe 320px avec scroll vertical. Simule un terminal.
- **`.user-action-confirm`** : masqué par défaut (`display: none`), affiché via JS pour les confirmations de suppression.
- **`#raspberry-select`** : select pleine largeur pour le choix du Raspberry Pi cible.

---

## Marketing — `marketing.css`

**Utilisé par :** `marketing_v2.html`

Styles de l'espace marketing, avec mise en page en colonnes de cartes.

### Layout

`.main-content` en flexbox avec `flex-grow: 1` et `gap: 20px`. Chaque `.card` prend `flex: 1` avec `width: 0` pour une répartition égale.

### Composants notables

- **`.upload-zone`** : zone de dépôt de fichier avec bordure en pointillés bleus (`#4a90e2`). Effet hover en bleu clair. Classe `.disabled` pour désactiver visuellement la zone.
- **`.card.sombre`** : variante sombre avec fond `#1a2b3c` et inputs en `#0e1a25`.

### Boutons

| Classe | Couleur | Usage |
|---|---|---|
| `.btn-primary` | `#4a90e2` (bleu) | Action principale |
| `.btn-secondary` | `#2ecc71` (vert) | Action secondaire, pleine largeur |

---

## Planning — `planning_style.css`

**Utilisé par :** `planning.html`

Styles du planning hebdomadaire interactif, la vue la plus complexe de l'application.

### Structure visuelle

```
.main-container
└── .controls-bar          (sticky, barre de contrôles)
└── .planning-container    (flex row, une colonne par jour)
    └── .day-column
        ├── .day-header    (nom du jour + input heure de départ)
        └── .drop-zone     (zone de glisser-déposer)
            └── .music-task (bloc musique draggable)
                └── .insert-task-btn (bouton + sur hover)
```

### Composants notables

- **`.day-column`** : colonne flexible, `min-width: 180px`, fond blanc, ombre légère. Le `.planning-container` est scrollable horizontalement si les colonnes débordent.
- **`.music-task`** : bloc musique draggable (`cursor: grab`), bordure gauche bleue. Au survol : agrandissement via `min-height: 45px !important` pour améliorer la lisibilité des blocs courts.
- **`.insert-task-btn`** : petit bouton `+` circulaire vert, `display: none` par défaut, affiché au survol d'un `.music-task` via CSS.
- **`.controls-bar`** : sticky en haut de page (`top: 0`, `z-index: 100`), fond bleu clair `#b5d3f0`.
- **Modale `.modal`** : fond semi-transparent avec `backdrop-filter: blur(2px)`. Contenu centré, largeur max `400px`. Contient les formulaires d'ajout/modification de musique.

### Support du mode sombre

Chaque composant possède une variante `.sombre` : `.day-column.sombre`, `.drop-zone.sombre`, `.modal-content.sombre`, `.add-music-btn.sombre`, etc.

---

## Alertes — `message_alert.css` & `message_alert.js`

Ces deux fichiers gèrent l'affichage et la disparition automatique des messages flash Flask.

### `message_alert.css`

| Classe | Couleur texte | Fond | Usage |
|---|---|---|---|
| `.alert-success` | `#155724` | `#d4edda` | Succès (vert) |
| `.alert-error` | `#721c24` | `#f8d7da` | Erreur (rouge) |
| `.alert-warning` | `#726b1c` | `#f4f4be` | Avertissement (jaune) |

Le bouton `.close-btn` est positionné en absolu en haut à droite de chaque alerte.

### `message_alert.js`

Au chargement du DOM, chaque `.alert-box` est programmée pour disparaître automatiquement après **4 secondes**, avec une transition d'opacité de 0.5s, puis suppression du DOM.

```
Affichage → 4000ms → fondu opacity 0 (500ms) → suppression du DOM
```

---

## Script global — `script.js`

**Utilisé par :** toutes les pages internes

Gère le mode sombre/clair, la navigation, le sélecteur de langue et les interactions de la navbar.

### Fonctions

#### `chgt_mode(event)`

Bascule entre mode clair et sombre selon la classe du bouton cliqué (`.mode-sombre` ou `.mode-clair`). Persiste le choix dans `localStorage` sous la clé `theme`.

#### `activerModeSombre()`

Ajoute la classe `.sombre` sur tous les éléments concernés : `body`, `.nav`, `.controls-bar`, `.planning-container`, toutes les `.card`, `.day-column`, `.drop-zone`, `.modal-content`, `.add-music-btn`, `.day-header`. Change l'icône du bouton en `☀️`.

#### `activerModeClair()`

Retire la classe `.sombre` des mêmes éléments. Change l'icône du bouton en `🌒`.

### Autres comportements

- **Sélecteur de langue** (`#select-langue`) : au changement, redirige vers `?lang=<valeur>`.
- **Bouton logout** (`#logout`) : redirige vers `/logout` au clic.
- **Rôle admin dans la navbar** (`.role_nav`) : si le texte est `"admin"`, ajoute un effet hover rouge et un clic redirige vers `/admin`.
- **Restauration du thème** : au chargement, lit `localStorage.getItem('theme')` et réapplique le mode sombre si nécessaire.

---

## Script planning — `planning_script.js`

> Le contenu de ce fichier n'était pas disponible dans les fichiers fournis. Il gère vraisemblablement les interactions drag & drop du planning hebdomadaire et les appels API vers `/move`, `/sync_day` et `/save_export`.

---

## Système de thèmes (clair / sombre)

Le thème est géré entièrement par ajout/retrait de la classe CSS `.sombre` via JavaScript. La préférence est persistée dans `localStorage`.

| Élément | Mode clair | Mode sombre |
|---|---|---|
| `body` | `#b5d3f0` | `#0e1a25` |
| `.nav` | `#267ac9` | `#083967` |
| `.card` | `#ffffff` | `#1a2b3c` |
| `.controls-bar` | `#b5d3f0` | `#0e1a25` |
| `.day-column` | `#ffffff` | `#1a2b3c` |
| `.drop-zone` | Gradient gris clair | Gradient noir |
| `.add-music-btn` | `#eeeeee` | `#0b4a85` |
| Inputs / selects | Standard | `#0e1a25` / texte blanc |

---

## Palette de couleurs

| Rôle | Couleur | Hex |
|---|---|---|
| Fond principal (clair) | Bleu clair | `#b5d3f0` |
| Fond principal (sombre) | Bleu nuit | `#0e1a25` |
| Navbar / accents | Bleu | `#267ac9` |
| Boutons danger / suppression | Rouge | `#d02424` / `#a33e3e` |
| Succès | Vert | `#2ecc71` / `#4CAF50` |
| Cartes sombres | Bleu foncé | `#1a2b3c` |
| Terminal | Noir / vert | `#0d0d0d` / `#00ff88` |