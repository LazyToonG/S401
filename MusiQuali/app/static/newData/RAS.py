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
    
    pygame.mixer.music.set_volume(0.0)
    play_message_tracks(channel_msg, paths)
    pygame.mixer.music.set_volume(MUSIC_VOLUME)
    log(f"--- MESSAGE termine, volume musique restauré ---")

# ------------------------------------------------------------------ main

def main():
    pygame.mixer.init()
    pygame.mixer.set_num_channels(2)

    channel_message = pygame.mixer.Channel(CHANNEL_MESSAGE)
    
    pygame.mixer.music.set_volume(MUSIC_VOLUME)
    channel_message.set_volume(MUSIC_VOLUME)

    log("=== Lecteur MusiQuali démarré (Mode Hybride Music/Mixer) ===")

    triggered_mu  = set()
    triggered_msg = set()
    current_day   = day_name()

    while True:
        # Récupération de l'heure système actuelle au format "HH:MM"
        now_str = datetime.now().strftime("%H:%M")

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
            slot_time = slot["time"]
            # Si le slot correspond à la minute pile et n'a pas encore été traité
            if slot_time == now_str and slot_time not in triggered_mu:
                triggered_mu.add(slot_time)
                path = mp3_path(slot["music"])
                log(f">>> MU slot {slot_time} : {slot['music']}")
                play_bg_music(path)

        # --- Vérifier les slots MESSAGE dus ---
        for slot in msg_slots:
            slot_time = slot["time"]
            if slot_time == now_str and slot_time not in triggered_msg:
                triggered_msg.add(slot_time)
                
                threading.Thread(
                    target=message_worker,
                    args=(channel_message, slot),
                    daemon=True
                ).start()

        # On dort 5 secondes pour laisser la minute s'écouler sans saturer le CPU
        time.sleep(5)

if __name__ == "__main__":
    main()