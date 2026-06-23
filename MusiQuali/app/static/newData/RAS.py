"""
lecteur.py — Lecteur audio dual-canal pour MusiQuali
======================================================
Canal Musique de fond (pygame.mixer.music) : gère MU.json (Format Plat).
Canal 1 (messages) : déclenche chaque message de MSG.json à l'heure pile.
"""
#allo
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

# ------------------------------------------------------------------ Canaux pygame
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

def today_mu_slots(json_data):
    return sorted(json_data.get(day_name(), []), key=lambda s: s["time"])

def today_msg_slots(json_data):
    return sorted(json_data.get(day_name(), []), key=lambda s: s["time"])

def load_json(path):
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)

def slot_datetime(time_str):
    h, m = map(int, time_str.split(":"))
    return datetime.now().replace(hour=h, minute=m, second=0, microsecond=0)

def mp3_path(filename):
    fname = filename if filename.lower().endswith(".mp3") else f"{filename}.mp3"
    return os.path.join(SOUND_DIR, fname)

def slot_is_due(slot_time_str):
    slot_dt = slot_datetime(slot_time_str)
    now = datetime.now()
    delta = (now - slot_dt).total_seconds()
    return 0 <= delta < 5  # fenêtre de 5 secondes

# ------------------------------------------------------------------ Lecture Musique

def play_bg_music(filepath):
    """Joue la musique sur le module dédié à la musique de fond."""
    if not os.path.isfile(filepath):
        log(f"MISSING {filepath}")
        return
    
    try:
        # charge et joue (remplace proprement le morceau en cours s'il y en a un)
        pygame.mixer.music.load(filepath)
        pygame.mixer.music.play()
        log(f"played (BG) {os.path.basename(filepath)}")
    except Exception as e:
        log(f"Erreur lecture musique {filepath} : {e}")

# ------------------------------------------------------------------ Lecture Messages

def play_message_tracks(channel, filepaths):
    """Joue les messages sur le canal d'effets (bloquant pour le thread message)."""
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
    """Gère l'abaissement du volume de la musique de fond pendant le message."""
    paths = [mp3_path(f) for f in slot["musics"]]

    log(f"--- MESSAGE slot {slot['time']} : {slot['musics']} ---")
    
    # Baisse le volume du module de musique globale
    pygame.mixer.music.set_volume(0.0)

    # Joue le message de manière bloquante
    play_message_tracks(channel_msg, paths)

    # Restaure le volume de la musique globale
    pygame.mixer.music.set_volume(MUSIC_VOLUME)
    log(f"--- MESSAGE termine, volume musique restauré ---")

# ------------------------------------------------------------------ main

def main():
    pygame.mixer.init()
    # On garde 2 canaux pour les effets/messages si besoin
    pygame.mixer.set_num_channels(2)

    channel_message = pygame.mixer.Channel(CHANNEL_MESSAGE)
    
    # Initialisation des volumes
    pygame.mixer.music.set_volume(MUSIC_VOLUME)
    channel_message.set_volume(MUSIC_VOLUME)

    log("=== Lecteur MusiQuali démarré (Mode Hybride Music/Mixer) ===")

    triggered_mu  = set()
    triggered_msg = set()
    current_day   = day_name()

    while True:
        now = datetime.now()

        if day_name() != current_day:
            log(f"=== Nouveau jour : {day_name()} ===")
            triggered_mu.clear()
            triggered_msg.clear()
            current_day = day_name()

        try:
            mu_data  = load_json(MU_JSON)
            msg_data = load_json(MSG_JSON)
        except Exception as e:
            log(f"Erreur lecture JSON : {e}")
            time.sleep(10)
            continue

        mu_slots  = today_mu_slots(mu_data)
        msg_slots = today_msg_slots(msg_data)

        # --- Vérifier les slots MUSIQUE dus ---
        for slot in mu_slots:
            if slot["time"] in triggered_mu:
                continue
            if slot_is_due(slot["time"]):
                triggered_mu.add(slot["time"])
                path = mp3_path(slot["music"])
                log(f">>> MU slot {slot['time']} : {slot['music']}")
                
                # Pas besoin de créer un thread complexe, l'appel de charge de la musique 
                # est quasi-instantané et non-bloquant avec pygame.mixer.music
                play_bg_music(path)

        # --- Vérifier les slots MESSAGE dus ---
        for slot in msg_slots:
            if slot["time"] in triggered_msg:
                continue
            if slot_is_due(slot["time"]):
                triggered_msg.add(slot["time"])
                
                # Le message tourne dans son thread pour ne pas bloquer la détection temporelle
                threading.Thread(
                    target=message_worker,
                    args=(channel_message, slot),
                    daemon=True
                ).start()

        time.sleep(2)

if __name__ == "__main__":
    main()