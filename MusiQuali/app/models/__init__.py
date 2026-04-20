import os, glob

## nous explicitons les éléments à charger automatiquement quand un import (export) est fait.
## l'environnement flask fonctionne ainsi
# __all__ = ("IndexController", "InfosController", "PokemonController")

# mais il est plus simple d'automatiser en prenant tous les fichiers python et leurs noms
__all__ = [os.path.basename(f)[:-3] for f in glob.glob(os.path.dirname(__file__) + "/*.py")]
