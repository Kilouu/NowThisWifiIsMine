from src.rogue_ap.fonctions import *
from src.rogue_ap.config_rogue import *

def launch_rogue_ap():
    print("[INFO] : Lancement de l'attaque Rogue AP... (En cours)")
    
    # Choice Interface
    interface = choix_network_interface()
    
    # Kill des process
    kill_process()

    # Lister les Réseaux Wifi
    bssid, channel, security, essid = lister_reseaux(interface, fichier_base="Capture/resultats", duree=20)
    print(f"BSSID: {bssid}, Channel: {channel}, Security: {security}, ESSID: {essid}")
    
    # Création du fichier de configuration Hostapd et Dnsmasq
    hostapd_process = None
    setup_rogue_ap(interface, channel, essid)