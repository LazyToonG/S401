document.addEventListener('DOMContentLoaded', function() {
    console.log("Script chargé correctement depuis le dossier static.");

    let availablePlaylists = {}; // Stockera les données reçues de l'API

    // --- Configuration des classes (doit correspondre au CSS) ---
    const CLASS_TASK = 'music-task';   // Remplace .music-item
    const CLASS_COLUMN = 'drop-zone'; // Cible la zone de drop spécifique

    // --- Gestion du Zoom (Variables globales) ---
    const zoomRange = document.getElementById('zoomRange');
    let currentScale = zoomRange ? parseFloat(zoomRange.value) : 1;
    if (zoomRange) zoomRange.max = 60; // Permet un zoom beaucoup plus puissant (1px/sec)

    // --- Fonction de recalcul des horaires (Séquentiel) ---
    function recalculateTimes(day) {
        let container = document.querySelector(`.${CLASS_COLUMN}[data-day="${day}"]`);
        if (!container) return;
        
        // Récupère l'heure de début de la colonne
        let currentSec = parseFloat(container.closest('.day-column').getAttribute('data-start-time')) || 0;
        
        // Décalage visuel du début de journée
        container.style.paddingTop = ((currentSec / 60) * currentScale) + 'px';
        
        container.querySelectorAll('.' + CLASS_TASK).forEach(item => {
            const h = Math.floor(currentSec / 3600);
            const m = Math.floor((currentSec % 3600) / 60);
            const timeStr = `${h.toString().padStart(2, '0')}:${m.toString().padStart(2, '0')}`;
            
            const st = item.querySelector('strong');
            if(st) st.innerText = timeStr;
            
            item.setAttribute('data-start-sec', currentSec);
            item.style.top = ''; // Nettoyage style inline pour éviter les décalages
            
            currentSec += parseFloat(item.getAttribute('data-duration'));
        });
    }

    // --- Gestion de l'insertion rapide ---
    let insertAfterItem = null;

    function addInsertButton(item) {
        if (item.querySelector('.insert-task-btn')) return;
        
        const btn = document.createElement('span');
        btn.className = 'insert-task-btn';
        btn.innerText = '+';
        btn.title = "Insérer en dessous";
        
        btn.onclick = (e) => {
            e.stopPropagation(); // Empêche l'ouverture de l'édition
            insertAfterItem = item;
            currentDropZone = item.parentElement;
            currentEditingItem = null;
            
            // Calcul de l'heure de début (fin de l'élément actuel)
            let startSec = parseFloat(item.getAttribute('data-start-sec')) || 0;
            startSec += parseFloat(item.getAttribute('data-duration')) || 0;
            
            const h = Math.floor(startSec / 3600) % 24;
            const m = Math.floor((startSec % 3600) / 60);
            const timeStr = `${h.toString().padStart(2, '0')}:${m.toString().padStart(2, '0')}`;

            prepareModalForAdd(timeStr);

            document.querySelector('#addMusicModal h3').innerText = "Insérer une musique";
            saveBtn.innerText = "Ajouter";
            if(deleteBtn) deleteBtn.style.display = "none";
            modal.style.display = "block";
        };
        item.appendChild(btn);
    }

    // --- Initialisation : Boutons et Start Time ---
    document.querySelectorAll('.day-column').forEach(col => {
        // Ajout du sélecteur d'heure de début
        const header = col.querySelector('.day-header');
        const timeInput = document.createElement('input');
        timeInput.type = 'time';
        timeInput.className = 'start-time-input';
        
        // Initialisation de la valeur
        let currentStartSec = parseFloat(col.getAttribute('data-start-time')) || 0;
        const h = Math.floor(currentStartSec / 3600) % 24;
        const m = Math.floor((currentStartSec % 3600) / 60);
        timeInput.value = `${h.toString().padStart(2, '0')}:${m.toString().padStart(2, '0')}`;

        timeInput.onchange = function() {
            const [nh, nm] = this.value.split(':').map(Number);
            col.setAttribute('data-start-time', nh * 3600 + nm * 60);
            const day = col.querySelector('.' + CLASS_COLUMN).getAttribute('data-day');
            recalculateTimes(day);
            syncDay(day);
        };
        timeInput.onmousedown = (e) => e.stopPropagation(); // Évite le drag
        header.appendChild(timeInput);

        // Recalcul immédiat pour corriger le positionnement au chargement
        const zone = col.querySelector('.' + CLASS_COLUMN);
        if (zone) {
            recalculateTimes(zone.getAttribute('data-day'));
        }

        // Ajout du bouton "Ajouter"
        const btn = document.createElement('button');
        btn.className = 'add-music-btn';
        btn.innerText = '+ Ajouter';
        btn.onclick = () => {
            currentDropZone = col.querySelector('.' + CLASS_COLUMN);
            insertAfterItem = null; // On ajoute à la fin
            currentEditingItem = null;
            
            // Calcul de l'heure de début pour la nouvelle tâche (fin de la dernière)
            let nextStartSec = parseFloat(col.getAttribute('data-start-time')) || 0;
            const tasks = currentDropZone.querySelectorAll('.' + CLASS_TASK);
            tasks.forEach(t => {
                nextStartSec += parseFloat(t.getAttribute('data-duration')) || 0;
            });
            const h = Math.floor(nextStartSec / 3600) % 24;
            const m = Math.floor((nextStartSec % 3600) / 60);
            const timeStr = `${h.toString().padStart(2, '0')}:${m.toString().padStart(2, '0')}`;

            prepareModalForAdd(timeStr);
            
            document.querySelector('#addMusicModal h3').innerText = "Ajouter une musique";
            saveBtn.innerText = "Ajouter";
            if(deleteBtn) deleteBtn.style.display = "none";
            modal.style.display = "block";
        };
        if (zone) zone.appendChild(btn);
    });

    // Ajout des boutons d'insertion aux tâches existantes
    document.querySelectorAll('.' + CLASS_TASK).forEach(addInsertButton);

    // --- Gestion du Zoom ---
    function checkZoomLevel(scale) {
        const container = document.querySelector('.planning-container');
        if (container) {
            if (scale < 2.5) container.classList.add('zoom-low');
            else container.classList.remove('zoom-low');
        }
    }

    if (zoomRange) {
        checkZoomLevel(currentScale);

        zoomRange.addEventListener('input', function() {
            const newScale = parseFloat(this.value);
            const container = document.querySelector('.planning-container');
            
            checkZoomLevel(newScale);

            // Calcul du centre pour le zoom
            const scrollTop = window.scrollY;
            const viewportHeight = window.innerHeight;
            const centerMinutes = (scrollTop + viewportHeight / 2) / currentScale;

            // Mise à jour des marqueurs d'heure
            document.querySelectorAll('.hour-marker').forEach(el => el.style.height = (60 * newScale) + 'px');

            // Mise à jour des tâches
            document.querySelectorAll('.' + CLASS_TASK).forEach(item => {
                const duration = parseFloat(item.getAttribute('data-duration'));
                const startSec = parseFloat(item.getAttribute('data-start-sec'));
                
                const newHeight = (duration / 60) * newScale;
                item.style.height = newHeight + 'px';
            });

            // Ajustement de la hauteur des colonnes
            document.querySelectorAll('.' + CLASS_COLUMN).forEach(col => {
                col.style.backgroundSize = `100% ${newScale}px`;
                
                const startSec = parseFloat(col.closest('.day-column').getAttribute('data-start-time')) || 0;
                col.style.paddingTop = ((startSec / 60) * newScale) + 'px';
            });

            // Ajustement du scroll
            window.scrollTo(0, (centerMinutes * newScale) - viewportHeight / 2);
            currentScale = newScale;
        });

        // Initialisation forcée pour appliquer les styles dès le chargement
        zoomRange.dispatchEvent(new Event('input'));
    }

    // --- Gestion de la Modale ---
    const modal = document.getElementById("addMusicModal");
    const closeBtn = document.querySelector(".close");
    const saveBtn = document.getElementById("saveMusicBtn");
    const deleteBtn = document.getElementById("deleteMusicBtn");
    let currentEditingItem = null;
    let currentDropZone = null;

    if (closeBtn) closeBtn.onclick = () => modal.style.display = "none";
    window.onclick = (e) => { if (e.target == modal) modal.style.display = "none"; };

    // --- Fonction de synchronisation avec le backend ---
    function syncDay(day) {
        let container = document.querySelector(`.${CLASS_COLUMN}[data-day="${day}"]`);
        if (!container) return;

        // Récupère toutes les tâches dans l'ordre du DOM
        const items = Array.from(container.querySelectorAll('.' + CLASS_TASK));

        const tasks = items.map(item => {
            const duration = item.getAttribute('data-duration');
            const path = item.getAttribute('data-path') || "";
            // Récupérer le titre et artiste directement des attributs data
            const title = item.getAttribute('data-title') || "";
            const artist = item.getAttribute('data-artist') || "";
            
            return { title: title, artist: artist, duration: duration, path: path };
        });

        // Récupération de l'heure de début
        const col = container.closest('.day-column');
        const startSec = parseFloat(col.getAttribute('data-start-time')) || 0;
        const h = Math.floor(startSec / 3600) % 24;
        const m = Math.floor((startSec % 3600) / 60);
        const startTimeStr = `${h.toString().padStart(2, '0')}:${m.toString().padStart(2, '0')}`;

        fetch('/sync_day', {
            method: 'POST',
            headers: {'Content-Type': 'application/json'},
            body: JSON.stringify({ day: day, tasks: tasks, start_time: startTimeStr })
        }).catch(e => console.error("Erreur sync backend", e));
    }

    // --- Gestion des Playlists (API & UI) ---
    
    // 1. Récupérer les playlists au chargement
    fetch('/api/playlists')
        .then(response => response.json())
        .then(data => {
            availablePlaylists = data;
            console.log("Playlists chargées :", availablePlaylists);
            // Mise à jour du select si la modale est déjà ouverte ou si le select existe déjà
            const playlistSelect = document.getElementById('playlistSelect');
            if (playlistSelect) {
                playlistSelect.innerHTML = '<option value="">-- Choisir une Playlist --</option>';
                for (let pl in availablePlaylists) {
                    const opt = document.createElement('option');
                    opt.value = pl;
                    opt.innerText = pl;
                    playlistSelect.appendChild(opt);
                }
            }
        })
        .catch(err => console.error("Erreur chargement playlists", err));

    // 2. Fonction pour transformer la modale en mode "Sélection Playlist"
    function prepareModalForAdd(startTimeStr) {
        if(document.getElementById('mStartTime')) {
            document.getElementById('mStartTime').value = startTimeStr;
            document.getElementById('mStartTime').readOnly = true;
        }
        
        // On vide les champs texte existants s'ils sont là et on injecte les selects
        const formContainer = document.querySelector('#addMusicModal .modal-content'); // Ajustez le sélecteur selon votre HTML réel
        
        // On cherche les inputs existants pour les cacher/remplacer
        const titleInput = document.getElementById('mTitle');
        const artistInput = document.getElementById('mArtist');
        const durationInput = document.getElementById('mDuration');

        if (titleInput) titleInput.closest('.form-group').style.display = 'none';
        if (artistInput) artistInput.closest('.form-group').style.display = 'none';
        if (durationInput) durationInput.readOnly = true; // La durée est fixée par la musique
        if (document.getElementById('playlistSelect')) document.getElementById('playlistSelect').style.display = 'inline-block';
        if (document.getElementById('musicSelect')) document.getElementById('musicSelect').style.display = 'inline-block';

        // Création/Récupération des Selects
        let playlistSelect = document.getElementById('playlistSelect');
        let musicSelect = document.getElementById('musicSelect');

        if (!playlistSelect) {
            // Injection dynamique si pas encore créés
            const container = titleInput ? titleInput.parentNode : formContainer;
            
            playlistSelect = document.createElement('select');
            playlistSelect.id = 'playlistSelect';
            playlistSelect.className = 'modal-select';
            playlistSelect.innerHTML = '<option value="">-- Choisir une Playlist --</option>';
            
            musicSelect = document.createElement('select');
            musicSelect.id = 'musicSelect';
            musicSelect.className = 'modal-select';
            musicSelect.innerHTML = '<option value="">-- D\'abord choisir une playlist --</option>';
            musicSelect.disabled = true;

            // Insertion dans le DOM (avant la durée par exemple)
            if (durationInput) {
                // On insère AVANT le groupe de la durée pour ne pas casser l'UI
                const durationGroup = durationInput.closest('.form-group');
                if (durationGroup) {
                    durationGroup.parentNode.insertBefore(playlistSelect, durationGroup);
                    durationGroup.parentNode.insertBefore(musicSelect, durationGroup);
                } else {
                    durationInput.parentNode.insertBefore(playlistSelect, durationInput);
                }
            }

            // Logique de changement
            playlistSelect.addEventListener('change', function() {
                const plName = this.value;
                musicSelect.innerHTML = '<option value="">-- Choisir une Musique --</option>';
                musicSelect.disabled = !plName;
                
                if (plName && availablePlaylists[plName]) {
                    availablePlaylists[plName].forEach((song, index) => {
                        const opt = document.createElement('option');
                        opt.value = index; // On utilise l'index pour retrouver l'objet complet
                        opt.innerText = `${song.name} (${song.duration}s)`;
                        musicSelect.appendChild(opt);
                    });
                }
            });

            musicSelect.addEventListener('change', function() {
                const plName = playlistSelect.value;
                const songIdx = this.value;
                if (plName && songIdx !== "" && availablePlaylists[plName][songIdx]) {
                    const song = availablePlaylists[plName][songIdx];
                    if(durationInput) durationInput.value = song.duration;
                }
            });
        }
        
        // Remplissage du select Playlist
        playlistSelect.innerHTML = '<option value="">-- Choisir une Playlist --</option>';
        for (let pl in availablePlaylists) {
            const opt = document.createElement('option');
            opt.value = pl;
            opt.innerText = pl;
            playlistSelect.appendChild(opt);
        }
    }

    // --- Interactions Clic (Ajout / Edition) ---
    document.querySelectorAll('.' + CLASS_COLUMN).forEach(zone => {
        zone.addEventListener('click', function(e) {
            if (isDragging) return; // Ne rien faire si on vient de glisser

            // Clic sur une tâche existante
            const musicItem = e.target.closest('.' + CLASS_TASK);
            if (musicItem) {
                e.stopPropagation();
                currentEditingItem = musicItem;
                currentDropZone = zone;
                
                // Récupération des infos (Heure dans strong, le reste après)
                const strong = musicItem.querySelector('strong');
                const timeText = strong ? strong.innerText : "00:00";
                
                // Clone pour extraire le texte sans le strong
                const clone = musicItem.cloneNode(true);
                if(clone.querySelector('strong')) clone.querySelector('strong').remove();
                const textContent = clone.innerText.trim(); 
                const parts = textContent.split(' - ');
                
                // En mode édition, on remet les inputs texte (ou on gère différemment, ici simple restore)
                if(document.getElementById('mStartTime')) {
                    document.getElementById('mStartTime').value = timeText;
                    document.getElementById('mStartTime').readOnly = true;
                }

                // Cacher les sélecteurs de playlist en mode édition
                if(document.getElementById('playlistSelect')) document.getElementById('playlistSelect').style.display = 'none';
                if(document.getElementById('musicSelect')) document.getElementById('musicSelect').style.display = 'none';
                
                // Pour l'édition, on affiche juste les infos (pas de changement de playlist implémenté ici pour simplifier)
                // Idéalement, il faudrait pré-sélectionner la playlist/musique si on avait l'info stockée
                if(document.getElementById('mTitle')) {
                    document.getElementById('mTitle').closest('.form-group').style.display = 'block';
                    document.getElementById('mTitle').value = parts[0] || "";
                    document.getElementById('mTitle').readOnly = true; // Empêcher modif manuelle
                }
                if(document.getElementById('mArtist')) {
                    document.getElementById('mArtist').closest('.form-group').style.display = 'block';
                    document.getElementById('mArtist').value = parts[1] || "";
                    document.getElementById('mArtist').readOnly = true; // Empêcher modif manuelle
                }
                if(document.getElementById('mDuration')) document.getElementById('mDuration').value = musicItem.getAttribute('data-duration');
                
                document.querySelector('#addMusicModal h3').innerText = "Modifier la programmation";
                saveBtn.innerText = "Enregistrer";
                deleteBtn.style.display = "block";
                modal.style.display = "block";
                return;
            }
        });
    });

    // --- Actions Boutons Modale ---
    if (deleteBtn) {
        deleteBtn.onclick = function() {
            if (currentEditingItem) {
                const day = currentEditingItem.closest('.' + CLASS_COLUMN).getAttribute('data-day');
                currentEditingItem.remove();
                recalculateTimes(day);
                syncDay(day);
                modal.style.display = "none";
            }
        };
    }

    if (saveBtn) {
        saveBtn.onclick = function() {
            let title, artist, duration, path;
            
            if (!currentDropZone) return alert("Erreur : Zone de dépôt non définie.");
            const day = currentDropZone.getAttribute('data-day');

            // Vérifie si on est en mode "Ajout via Playlist" ou "Edition manuelle"
            const playlistSelect = document.getElementById('playlistSelect');
            
            // Si on ajoute (pas d'item en cours d'édition) et qu'une playlist est sélectionnée
            if (!currentEditingItem && playlistSelect && playlistSelect.style.display !== 'none') {
                const plName = playlistSelect.value;
                const musicSelect = document.getElementById('musicSelect');
                const songIdx = musicSelect.value;
                
                if (!plName || songIdx === "") return alert("Veuillez sélectionner une musique.");
                
                const song = availablePlaylists[plName][songIdx];
                title = song.name;
                artist = song.artist;
                duration = parseInt(song.duration);
                path = song.path;
            } else {
                // Mode Edition (Legacy ou déplacement simple)
                title = document.getElementById('mTitle').value;
                artist = document.getElementById('mArtist').value;
                duration = parseInt(document.getElementById('mDuration').value);
                path = currentEditingItem ? currentEditingItem.getAttribute('data-path') : "";
            }

            if (!title || !duration) return alert("Titre et durée requis.");

            let item = currentEditingItem;
            if (!item) {
                item = document.createElement('div');
                item.className = CLASS_TASK;
                
                if (insertAfterItem && insertAfterItem.parentNode === currentDropZone) {
                    // Insertion après l'élément ciblé
                    if (insertAfterItem.nextSibling) {
                        currentDropZone.insertBefore(item, insertAfterItem.nextSibling);
                    } else {
                        currentDropZone.appendChild(item);
                    }
                } else {
                    // Ajout classique à la fin (avant le bouton Ajouter)
                    const btn = currentDropZone.querySelector('.add-music-btn');
                    if (btn) currentDropZone.insertBefore(item, btn);
                    else currentDropZone.appendChild(item);
                }
            }

            item.setAttribute('data-duration', duration);
            item.setAttribute('data-path', path); // Sauvegarde du chemin
            item.setAttribute('data-title', title); // Sauvegarde du titre
            item.setAttribute('data-artist', artist); // Sauvegarde de l'artiste
            item.style.height = ((duration / 60) * currentScale) + 'px';
            item.innerHTML = `<strong>--:--</strong><br>${title} - ${artist}`;
            addInsertButton(item); // Ré-ajout du bouton après modification du HTML
            
            recalculateTimes(day);
            syncDay(day);
            modal.style.display = "none";
        };
    }

    // --- Drag & Drop ---
    let isDragging = false;
    let dragItem = null;
    let dragStartDay = null;

    document.addEventListener('mousedown', function(e) {
        const item = e.target.closest('.' + CLASS_TASK);
        if (item) {
            isDragging = false;
            dragItem = item;
            dragStartDay = item.parentElement.getAttribute('data-day');
        }
    });

    document.addEventListener('mousemove', function(e) {
        if (dragItem && !isDragging) {
            isDragging = true;
            dragItem.style.opacity = '0.5';
            document.body.style.cursor = 'grabbing';
        }
        if (isDragging && dragItem) {
            const elemBelow = document.elementFromPoint(e.clientX, e.clientY);
            const dropZone = elemBelow ? elemBelow.closest('.' + CLASS_COLUMN) : null;
            if (dropZone) {
                // Logique de tri : trouver l'élément le plus proche
                const siblings = [...dropZone.querySelectorAll('.' + CLASS_TASK + ':not(.dragging)')];
                const nextSibling = siblings.find(sibling => {
                    const rect = sibling.getBoundingClientRect();
                    return e.clientY < rect.top + rect.height / 2;
                });
                
                if (nextSibling) dropZone.insertBefore(dragItem, nextSibling);
                else {
                    const btn = dropZone.querySelector('.add-music-btn');
                    if (btn) dropZone.insertBefore(dragItem, btn);
                    else dropZone.appendChild(dragItem);
                }
            }
        }
    });

    document.addEventListener('mouseup', function(e) {
        if (dragItem && isDragging) {
            const dropZone = dragItem.parentElement;
            
            // Recalcul des horaires et sauvegarde
            const currentDay = dropZone.getAttribute('data-day');
            if (dragStartDay !== currentDay) {
                recalculateTimes(dragStartDay);
                syncDay(dragStartDay);
            }
            recalculateTimes(currentDay);
            syncDay(currentDay);

            dragItem.style.pointerEvents = ''; 
            dragItem.style.opacity = ''; 
            document.body.style.cursor = ''; 
            dragItem = null;
            setTimeout(() => isDragging = false, 100);
        } else {
            dragItem = null;
        }
    });

    // --- Sauvegarde ---
    const saveFileBtn = document.getElementById('saveToFileBtn');
    if (saveFileBtn) {
        saveFileBtn.addEventListener('click', function() {
            fetch('/save_export', { method: 'POST' })
            .then(response => response.json())
            .then(data => {
                if (data.success) {
                    alert(data.message);
                } else {
                    alert("Erreur : " + data.message);
                }
            })
            .catch(e => alert("Erreur lors de l'exportation"));
        });
    }
});