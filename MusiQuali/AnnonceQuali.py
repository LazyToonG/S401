import time
import unittest

class AnnonceQuali:
    """
    Classe gérant la lecture des annonces et la gestion de la musique de fond.
    """
    
    def __init__(self):
        # Par défaut, on imagine que la musique est activée
        self.musique_en_cours = True

    def mute_musique(self):
        """Coupe la musique de fond."""
        self.musique_en_cours = False
        print("[Système] 🔇 Musique coupée (Mute).")

    def unmute_musique(self):
        """Relance la musique de fond."""
        self.musique_en_cours = True
        print("[Système] 🔊 Musique réactivée (Unmute).")

    def lire_annonce(self, message_annonce):
        """
        Lit une annonce en coupant la musique avant, 
        puis en la remettant à la fin.
        """
        print("\n--- Début de l'annonce ---")
        
        self.mute_musique()
        
        print(f"[Voix] : {message_annonce}")
        # On simule le temps de l'annonce
        time.sleep(2) 

        self.unmute_musique()
        
        print("--- Fin de l'annonce ---\n")


# --- PARTIE TESTS UNITAIRES ---
class TestAnnonceQuali(unittest.TestCase):
    
    def test_mute_et_unmute(self):
        systeme = AnnonceQuali()
        
        # Vérifie que la musique est activée au début
        self.assertTrue(systeme.musique_en_cours)

        # Vérifie que le mute fonctionne
        systeme.mute_musique()
        self.assertFalse(systeme.musique_en_cours)

        # Vérifie que le unmute fonctionne
        systeme.unmute_musique()
        self.assertTrue(systeme.musique_en_cours)

if __name__ == '__main__':
    # Démonstration quand on lance le fichier
    lecteur = AnnonceQuali()
    lecteur.lire_annonce("Attention, fermeture imminente.")

    print("\n--- Lancement des tests ---")
    unittest.main(exit=False)
    