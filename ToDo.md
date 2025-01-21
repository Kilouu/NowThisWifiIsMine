# Tâches à faire

## Lancer le serveur Python
```bash
sudo python3 -m http.server 80 --directory src/rogue_ap/WebsiteRogue/index.html
```

## Le site Web
- `index.html` et `fichier de capture.php` qui stocke dans `log.txt`

## Configurer l'IP sur l'interface wlan0
```bash
sudo ifconfig wlan0 192.168.1.1
```

## Augmenter la puissance du signal réseau

### Étape 1 : Vérifiez les limites régionales
La réglementation limite la puissance maximale. Changez la région pour une limite plus élevée :
```bash
sudo iw reg set BO
```
**Note:** BO (Bolivie) permet une puissance élevée dans certains cas. Utilisez avec précaution.

### Étape 2 : Augmentez la puissance
```bash
sudo iwconfig wlan0 txpower 30
```
**Note:** 30 dBm correspond à 1 watt, la limite légale dans certains pays.

## Utiliser un canal moins encombré
Un canal Wi-Fi surchargé peut réduire l’efficacité :
```bash
iwlist wlan0 scan | grep Frequency
```
Choisissez un canal avec peu de réseaux voisins et configurez-le dans votre `hostapd.conf` :
```conf
channel=6
```

## Vérifiez la configuration de hostapd
Dans le fichier de configuration `hostapd.conf` :
```conf
hw_mode=g
ieee80211n=1
```