import os



# Suppression du fichier de configuration Hostapd
def remove_hostapd_conf():
    try:
        os.remove("RogueAP/hostapd.conf")
        print("[SUCCESS] : Fichier de configuration Hostapd supprimé avec succès.")
    except FileNotFoundError:
        print("[ERROR] : Fichier de configuration Hostapd introuvable.")
    except Exception as e:
        print(f"[ERROR] : Une erreur s'est produite lors de la suppression du fichier Hostapd : {e}")


# Suppression du fichier de configuration Dnsmasq
def remove_dnsmasq_conf():
    try:
        os.remove("RogueAP/dnsmasq.conf")
        print("[SUCCESS] : Fichier de configuration Dnsmasq supprimé avec succès.")
    except FileNotFoundError:
        print("[ERROR] : Fichier de configuration Dnsmasq introuvable.")
    except Exception as e:
        print(f"[ERROR] : Une erreur s'est produite lors de la suppression du fichier Dnsmasq : {e}")


# Suppression des règles iptables
def iptables_unconf(interface):
    commands = [
        # Désactivation du forwarding IP
        "sudo sysctl -w net.ipv4.ip_forward=0",
        
        # Suppression du masquerading NAT
        "sudo iptables -t nat -D POSTROUTING -o eth0 -j MASQUERADE",
        
        # Suppression de l'autorisation du trafic venant de l'interface AP
        f"sudo iptables -D FORWARD -i {interface} -j ACCEPT",
        
        # Suppression de la redirection du trafic HTTP (port 80)
        "sudo iptables -t nat -D PREROUTING -p tcp --dport 80 -j DNAT --to-destination 192.168.1.1",
        
        # Suppression de la redirection du trafic HTTPS (port 443)
        "sudo iptables -t nat -D PREROUTING -p tcp --dport 443 -j DNAT --to-destination 192.168.1.1",
    ]

    for command in commands:
        if os.system(command) != 0:
            print(f"[ERROR] : Échec de l'exécution de la commande : {command}")
        else:
            print(f"[SUCCESS] : Commande exécutée avec succès : {command}")

    print("[INFO] : Toutes les règles iptables ont été supprimées.")


# Stop le service Dnsmasq
def stop_dnsmasq():
    if os.system("sudo systemctl stop dnsmasq") != 0:
        print("[ERROR] : Échec de l'arrêt du service Dnsmasq.")
    else:
        print("[SUCCESS] : Service Dnsmasq stoppé avec succès.")
        

# Stop le service Hostapd
def stop_hostapd():
    if os.system("sudo systemctl stop hostapd") != 0:
        print("[ERROR] : Échec de l'arrêt du service Hostapd.")
    else:
        print("[SUCCESS] : Service Hostapd stoppé avec succès.")


# Stop le service Apache2
def stop_http_server():
    if os.system("sudo systemctl stop apache2.service") != 0:
        print("[ERROR] : Échec de l'arrêt du service Apache2.")
    else:
        print("[SUCCESS] : Service Apache2 stoppé avec succès.")


# Suppression des fichiers du site web
def remove_website_files():
    try:
        os.remove("/var/www/html/index.html")
        os.remove("/var/www/html/capture.php")
        os.remove("/var/www/html/log.txt")
        print("[SUCCESS] : Fichiers du site web supprimés avec succès.")
    except FileNotFoundError:
        print("[ERROR] : Fichiers du site web introuvables.")
    except Exception as e:
        print(f"[ERROR] : Une erreur s'est produite lors de la suppression des fichiers du site web : {e}")




# Enleve le setup du Rogue AP
def unsetup_rogue_ap(interface):
    
    
    stop_http_server()
    stop_dnsmasq()
    stop_hostapd()
    
    remove_hostapd_conf()
    remove_dnsmasq_conf()
    remove_website_files()
    
    iptables_unconf(interface)