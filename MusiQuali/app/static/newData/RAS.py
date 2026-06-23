"""
lecteur.py — Lecteur audio dual-canal pour MusiQuali
======================================================
Canal Musique de fond (pygame.mixer.music) : gère MU.json (Format Plat).
Canal 1 (messages) : déclenche chaque message de MSG.json à l'heure pile.
"""
#allo arthuuuuur
import os
import json
import time
import threading
from datetime import datetime, date

os.environ["PYGAME_HIDE_SUPPORT_PROMPT"] = "hide"
import pygame

# ------------------------------------------------------------------ Chemins
BASE_DIR    = os.path.dirname(os.path.abspath(__file__))
MU_JSON     = os.path.join(BASE_DIR, "MU.json")
MSG_JSON    = os.path.join(BASE_DIR, "MSG.json")
SOUND_DIR   = os.path.join(BASE_DIR, "rasSound")
LOG_DIR     = os.path.join(BASE_DIR, "logs")

# ------------------------------------------------------------------ Configuration
CHANNEL_MESSAGE = 1
MUSIC_VOLUME = 1.0

# ------------------------------------------------------------------ Logging

def get_log_path():
    return os.path.join(LOG_DIR, f"logs[{date.today().isoformat()}].txt")

def log(msg):
    os.makedirs(LOG_DIR, exist_ok=True)
    line = f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] {msg}"
    print(line)
    with open(get_log_path(), "a", encoding="utf-8") as f:
        f.write(line + "\n")

# ------------------------------------------------------------------ fonctions

def day_name():
    """Retourne le nom du jour en anglais lowercase (ex: 'monday')."""
    return datetime.now().strftime("%A").lower()

def load_json(path):
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)

def mp3_path(filename):
    fname = filename if filename.lower().endswith(".mp3") else f"{filename}.mp3"
    return os.path.join(SOUND_DIR, fname)

# ------------------------------------------------------------------ Lecture Musique

def play_bg_music(filepath):
    if not os.path.isfile(filepath):
        log(f"MISSING {filepath}")
        return
    
    try:
        pygame.mixer.music.load(filepath)
        pygame.mixer.music.play()
        log(f"played (BG) {os.path.basename(filepath)}")
    except Exception as e:
        log(f"Erreur lecture musique {filepath} : {e}")

# ------------------------------------------------------------------ Lecture Messages

def play_message_tracks(channel, filepaths):
    for path in filepaths:
        if not os.path.isfile(path):
            log(f"MISSING {path}")
            continue
        sound = pygame.mixer.Sound(path)
        channel.play(sound)
        log(f"played MSG  {os.path.basename(path)}")
        while channel.get_busy():
            time.sleep(0.1)

def message_worker(channel_msg, slot):
    paths = [mp3_path(f) for f in slot["musics"]]
    log(f"--- MESSAGE slot {slot['time']} : {slot['musics']} ---")
    
    # Évanouissement / Mute de la musique de fond
    pygame.mixer.music.set_volume(0.0)
    
    # Lecture séquentielle des messages
    play_message_tracks(channel_msg, paths)
    
    # Restauration du volume
    pygame.mixer.music.set_volume(MUSIC_VOLUME)
    log(f"--- MESSAGE termine, volume musique restauré ---")

# ------------------------------------------------------------------ main

def main():
    pygame.mixer.init()
    pygame.mixer.set_num_channels(2)

    channel_message = pygame.mixer.Channel(CHANNEL_MESSAGE)
    
    pygame.mixer.music.set_volume(MUSIC_VOLUME)
    channel_message.set_volume(MUSIC_VOLUME)

    log("=== Lecteur MusiQuali démarré (Mode Dictionnaire Sécurisé) ===")

    last_triggered_mu  = ""
    last_triggered_msg = ""
    current_day   = day_name()

    while True:
        # Heure de référence pour ce cycle de boucle (Format unique ex: "16:19")
        now_str = datetime.now().strftime("%H:%M")

        # Gestion du changement de jour
        if day_name() != current_day:
            log(f"=== Nouveau jour : {day_name()} ===")
            last_triggered_mu  = ""
            last_triggered_msg = ""
            current_day = day_name()

        # Lecture défensive des fichiers d'export
        try:
            mu_data  = load_json(MU_JSON)
            msg_data = load_json(MSG_JSON)
        except Exception as e:
            log(f"Erreur lecture JSON : {e}")
            time.sleep(5)
            continue

        # Récupération de la liste brute pour le jour courant
        raw_mu_slots  = mu_data.get(current_day, [])
        raw_msg_slots = msg_data.get(current_day, [])

        # CONVERSION EN DICTIONNAIRE UNIQUE (Clé: "HH:MM" -> Valeur: l'objet slot)
        # Cela écrase de fait tout doublon de structure présent dans le fichier JSON
        mu_dict  = {slot["time"]: slot for slot in raw_mu_slots}
        msg_dict = {slot["time"]: slot for slot in raw_msg_slots}

        # --- Déclenchement de la MUSIQUE ---
        if now_str in mu_dict and now_str != last_triggered_mu:
            last_triggered_mu = now_str  # Verrouillage immédiat
            slot = mu_dict[now_str]
            path = mp3_path(slot["music"])
            log(f">>> MU slot {now_str} : {slot['music']}")
            play_bg_music(path)

        # --- Déclenchement des MESSAGES ---
        if now_str in msg_dict and now_str != last_triggered_msg:
            last_triggered_msg = now_str  # Verrouillage immédiat
            slot = msg_dict[now_str]
            
            threading.Thread(
                target=message_worker,
                args=(channel_message, slot),
                daemon=True
            ).start()

        # Pause d'une seconde complète avant de réévaluer l'horloge système
        time.sleep(1)

if __name__ == "__main__":
    main()