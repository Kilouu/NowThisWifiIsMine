import os
import time
import subprocess

'''
sudo iptables -t nat -D POSTROUTING -o eth0 -j MASQUERADE
sudo iptables -D FORWARD -i wlan0 -j ACCEPT
sudo iptables -t nat -D PREROUTING -p tcp --dport 80 -j DNAT --to-destination 192.168.1.1

sudo iptables -t nat -L POSTROUTING --line-numbers
sudo iptables -L FORWARD --line-numbers
sudo iptables -t nat -L PREROUTING --line-numbers
'''

# Supprimer les règles iptables
def iptables_unconf(interface):
    # Suppression des règles iptables
    command1 = "sudo iptables -t nat -D POSTROUTING -o eth0 -j MASQUERADE"
    if os.system(command1) != 0:
        print(f"[ERROR] : Échec de l'exécution de la commande : {command1}")
    else:
        print(f"[SUCCESS] : Commande exécutée avec succès : {command1}")

    command2 = f"sudo iptables -D FORWARD -i {interface} -j ACCEPT"
    if os.system(command2) != 0:
        print(f"[ERROR] : Échec de l'exécution de la commande : {command2}")
    else:
        print(f"[SUCCESS] : Commande exécutée avec succès : {command2}")

    command3 = "sudo iptables -t nat -D PREROUTING -p tcp --dport 80 -j DNAT --to-destination 192.168.1.1"
    if os.system(command3) != 0:
        print(f"[ERROR] : Échec de l'exécution de la commande : {command3}")
    else:
        print(f"[SUCCESS] : Commande exécutée avec succès : {command3}")


# Stop le service Dnsmasq
def stop_dnsmasq():
    if os.system("sudo systemctl stop dnsmasq") != 0:
        print("[ERROR] : Échec de l'arrêt du service Dnsmasq.")
    else:
        print("[SUCCESS] : Service Dnsmasq stoppé avec succès.")


# Enleve le setup du Rogue AP
def unsetup_rogue_ap(interface):
    time.sleep(120)
    stop_dnsmasq()
    iptables_unconf(interface)