"""
lecteur.py — Lecteur audio dual-canal pour MusiQuali
======================================================
Canal 0 (musique) : joue les playlists de MU.json à l'heure programmée,
s'arrête à la fin, attend le prochain slot.
Canal 1 (messages) : déclenche chaque message de MSG.json à l'heure pile,
met le volume du canal musique à 0 le temps du message,
puis le remonte.
 attendu  :
    rasData/MU.json
    rasData/MSG.json
    rasData/rasSound/les mp3         
"""

import os
import json
import time
import threading
from datetime import datetime, date

os.environ["PYGAME_HIDE_SUPPORT_PROMPT"] = "hide"
import pygame

# ------------------------------------------------------------------ Chemins
BASE_DIR    = os.path.dirname(os.path.abspath(__file__))
MU_JSON     = os.path.join(BASE_DIR, "rasData", "MU.json")
MSG_JSON    = os.path.join(BASE_DIR, "rasData", "MSG.json")
SOUND_DIR   = os.path.join(BASE_DIR, "rasData", "rasSound")
LOG_DIR     = os.path.join(BASE_DIR, "logs")

# ------------------------------------------------------------------ Canaux pygame
CHANNEL_MUSIC   = 0
CHANNEL_MESSAGE = 1

MUSIC_VOLUME = 1.0  # volume normal du canal musique (0.0 → 1.0)

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

def today_slots(json_data):
    """
    Retourne:
    {"time": "HH:MM", "musics": ["a.mp3", "b.mp3"]}
    """
    return sorted(json_data.get(day_name(), []), key=lambda s: s["time"])

def load_json(path):
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)

def slot_datetime(time_str):
    """Construit un datetime pour aujourd'hui ."""
    h, m = map(int, time_str.split(":"))
    return datetime.now().replace(hour=h, minute=m, second=0, microsecond=0)

def mp3_path(filename):
    """Retourne le chemin complet d'un fichier mp3 (en ajoutant .mp3 si absent en cas de douille)."""
    fname = filename if filename.lower().endswith(".mp3") else f"{filename}.mp3"
    return os.path.join(SOUND_DIR, fname)

# ------------------------------------------------------------------ Lecture

def play_tracks_on_channel(channel, filepaths):
    """
    Joue une liste de fichiers mp3 séquentiellement sur un canal pygame donné.
    Bloquant jusqu'à la fin de toute la séquence.
    """
    for path in filepaths:
        if not os.path.isfile(path):
            log(f"MISSING {path}")
            continue

        sound = pygame.mixer.Sound(path)
        channel.play(sound)
        log(f"played  {os.path.basename(path)}")

        # Attendre la fin de cette piste
        while channel.get_busy():
            time.sleep(0.1)

# ------------------------------------------------------------------ Canal message 

def message_worker(channel_msg, channel_music, slot):
    """
    Joue un slot de message sur channel_msg.
    Pendant ce temps, met le volume de channel_music à 0 puis le restaure.
    """
    paths = [mp3_path(f) for f in slot["musics"]]

    log(f"--- MESSAGE slot {slot['time']} : {slot['musics']} ---")
    channel_music.set_volume(0.0)

    play_tracks_on_channel(channel_msg, paths)

    channel_music.set_volume(MUSIC_VOLUME)
    log(f"--- MESSAGE termine, volume musique restauré ---")

# ------------------------------------------------------------------ main

def main():
    pygame.mixer.init()
    pygame.mixer.set_num_channels(2)

    channel_music   = pygame.mixer.Channel(CHANNEL_MUSIC)
    channel_message = pygame.mixer.Channel(CHANNEL_MESSAGE)

    channel_music.set_volume(MUSIC_VOLUME)
    channel_message.set_volume(MUSIC_VOLUME)

    log("=== Lecteur MusiQuali démarré ===")

    # Garde une trace des slots déjà déclenchés (évite les doublons dans la même journée)
    triggered_mu  = set()   # "HH:MM"
    triggered_msg = set()   # "HH:MM"
    current_day   = day_name()

    while True:
        now = datetime.now()

        # Reset au changement de jour
        if day_name() != current_day:
            log(f"=== Nouveau jour : {day_name()} ===")
            triggered_mu.clear()
            triggered_msg.clear()
            current_day = day_name()

        # Recharge les JSON à chaque cycle (prend en compte les updates du serveur)
        try:
            mu_data  = load_json(MU_JSON)
            msg_data = load_json(MSG_JSON)
        except Exception as e:
            log(f"Erreur lecture JSON : {e}")
            time.sleep(10)
            continue

        mu_slots  = today_slots(mu_data)
        msg_slots = today_slots(msg_data)

        # --- Vérifier les slots MUSIQUE dus ---
        for slot in mu_slots:
            if slot["time"] in triggered_mu:
                continue
            if now >= slot_datetime(slot["time"]):
                triggered_mu.add(slot["time"])
                paths = [mp3_path(f) for f in slot["musics"]]
                log(f">>> MU slot {slot['time']} : {slot['musics']}")
                # Lance la playlist musique dans un thread pour ne pas bloquer la boucle
                threading.Thread(
                    target=play_tracks_on_channel,
                    args=(channel_music, paths),
                    daemon=True
                ).start()

        # --- Vérifier les slots MESSAGE dus ---
        for slot in msg_slots:
            if slot["time"] in triggered_msg:
                continue
            if now >= slot_datetime(slot["time"]):
                triggered_msg.add(slot["time"])
                # Le message tourne dans son propre thread pour rester non-bloquant,
                # mais il gère lui-même le volume de channel_music de façon synchrone
                threading.Thread(
                    target=message_worker,
                    args=(channel_message, channel_music, slot),
                    daemon=True
                ).start()

        time.sleep(2)

if __name__ == "__main__":
    main()