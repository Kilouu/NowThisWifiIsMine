import subprocess
import os
import json
from fonctions import *

if __name__ == "__main__":
    
    # Quel Attaque va être lancé
    # type_attaque = choix_attaque()
    
    # Choix de L'interface
    interface = choix_network_interface()

    # Kill des process
    kill_process()

    # Active le mode monitor sur l'interface séléctionné
    start_mode_monitor(interface)
    
    # Lister les Réseaux Wifi
    lister_reseaux(interface, fichier_base="Capture/resultats", duree=20, dossier_json="Json")
    
    
    
    # Choix de l'attaque
    attack_type = choose_attack_type()
    
    
    # Capture depuis la Target
    capture_from_target_json(interface, attack_type)
    
    

    

    
    
    # Stop le mode monitor sur l'interface séléctionné
    stop_mode_monitor(interface)
    