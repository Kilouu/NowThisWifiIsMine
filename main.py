from fonctions import *

if __name__ == "__main__":
    # Choix de L'interface
    interface = choix_network_interface()

    # Kill des process
    kill_process()

    # Active le mode monitor sur l'interface sélectionnée
    start_mode_monitor(interface)

    # Lister les Réseaux Wifi
    lister_reseaux(interface, fichier_base="Capture/resultats", duree=20, dossier_json="Json")

    # Choix de l'attaque
    attack_type = choose_attack_type()

    # Launch Attack
    if attack_type == "WPA":
        wpa_launch_attack(interface)
    elif attack_type == "WEP":
        wep_launch_attack(interface)
    elif attack_type == "WPS":
        print("Lancement de l'attaque WPS... (En cours)")

    # Stop le mode monitor sur l'interface sélectionnée
    stop_mode_monitor(interface)
