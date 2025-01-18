import subprocess
import os
import time

# Ajout Des Success color
ERROR_COLOR = "\033[91m"    # Red
INFO_COLOR = "\033[93m"     # Yellow
RESET_COLOR = "\033[0m"     # Reset
SUCCESS_COLOR = "\033[92m"  # Green

# Creer les Répertoires Manquants
def create_directories():
    os.makedirs("Capture", exist_ok=True)
    os.makedirs("Result", exist_ok=True)
    os.makedirs("Target", exist_ok=True)
    os.makedirs("Wordlist", exist_ok=True)
    print(f"{SUCCESS_COLOR}[SUCCESS]{RESET_COLOR} : Répertoires créés avec succès")

# Capture les Différents réseaux WIFI disponible pendant 20 Secondes
def capture_wifi_networks(interface, fichier_base, duree):
    print(f"{INFO_COLOR}Recherche des réseaux Wi-Fi sur {interface} pendant {duree} secondes...{RESET_COLOR}")
    process = subprocess.Popen(
        ["sudo", "airodump-ng", "--write", fichier_base, interface],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE
    )
    time.sleep(duree)
    process.terminate()
    print(f"{SUCCESS_COLOR}[SUCCESS]{RESET_COLOR} : La capture a été enregistrée")

# Lit le fichier CSV et extrait les info Importante
def read_csv_and_extract_networks(fichier_base):
    csv_file = f"{fichier_base}-01.csv"
    reseaux = []
    if os.path.exists(csv_file):
        with open(csv_file, "r") as file:
            lines = file.readlines()
            start_reading = False
            for line in lines:
                if start_reading:
                    parts = [p.strip() for p in line.split(",")]
                    if len(parts) > 13 and parts[0]:
                        reseaux.append({
                            "BSSID": parts[0],
                            "Channel": parts[3],
                            "Security": parts[5],
                            "ESSID": parts[13]
                        })
                elif line.strip() == "":
                    start_reading = True
    return reseaux

# Affiche les réseaux Disponible et enregistre dans un Fichier Target
def display_networks_and_select_target(reseaux):
    if not reseaux:
        print(f"{ERROR_COLOR}Aucun réseau détecté.{RESET_COLOR}")
        return None

    print(f"{INFO_COLOR}\nRéseaux Wi-Fi disponibles:{RESET_COLOR}")
    print(f"{'Numéro':<6} {'BSSID':<20} {'Channel':<8} {'Security':<10} {'ESSID':<20}")
    print("-" * 70)
    for idx, reseau in enumerate(reseaux, start=1):
        print(f"{idx:<6} {reseau['BSSID']:<20} {reseau['Channel']:<8} {reseau['Security']:<10} {reseau['ESSID']:<20}")

    while True:
        try:
            choice = int(input("\nChoisissez un réseau par son numéro : "))
            if 1 <= choice <= len(reseaux):
                target = reseaux[choice - 1]
                return target['BSSID'], target['Channel'], target['Security'], target['ESSID']
            else:
                print(f"{ERROR_COLOR}Veuillez entrer un numéro valide.{RESET_COLOR}")
        except ValueError:
            print(f"{ERROR_COLOR}Veuillez entrer un nombre valide.{RESET_COLOR}")

# Supprime les fichiers de Capture
def clean_capture_directory():
    for fichier in os.listdir("Capture"):
        chemin_fichier = os.path.join("Capture", fichier)
        try:
            os.remove(chemin_fichier)
            print(f"{SUCCESS_COLOR}[SUCCESS]{RESET_COLOR} : {chemin_fichier} supprimé")
        except Exception as e:
            print(f"{ERROR_COLOR}[ERREUR] Impossible de supprimer {chemin_fichier} : {e}{RESET_COLOR}")

# Supprime les fichiers de Result
def clean_result_directory():
    for fichier in os.listdir("Result"):
        chemin_fichier = os.path.join("Result", fichier)
        try:
            os.remove(chemin_fichier)
            print(f"{SUCCESS_COLOR}[SUCCESS]{RESET_COLOR} : {chemin_fichier} supprimé")
        except Exception as e:
            print(f"{ERROR_COLOR}[ERREUR] Impossible de supprimer {chemin_fichier} : {e}{RESET_COLOR}")
    