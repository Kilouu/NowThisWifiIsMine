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
    
    
    # Launch Attack
    if attack_type == "WPA":
        capture_from_target_json_wpa(interface)
        selected_wordlist = list_and_choose_wordlist()
        
        if selected_wordlist:
            print(f"Utilisation de la wordlist : {selected_wordlist}")
            crack_handshake_with_wordlist(selected_wordlist)
            
        else:
            print("Aucune wordlist sélectionnée.")
        
    elif attack_type == "WEP":
        capture_from_target_json_wep(interface)

        
    elif attack_type == "WPS":
        print("Lancement de l'attaque WPS... (En cours)")
    
    
    

    

    

    
    
    # Stop le mode monitor sur l'interface séléctionné
    stop_mode_monitor(interface)