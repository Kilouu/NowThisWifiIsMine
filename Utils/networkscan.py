import subprocess
import os
import time


# Creer les Répertoires Manquants
def create_directories():
    os.makedirs("Capture", exist_ok=True)
    os.makedirs("Result", exist_ok=True)
    os.makedirs("Target", exist_ok=True)
    os.makedirs("Station", exist_ok=True)


# Capture les Différents réseaux WIFI disponible pendant 20 Secondes
def capture_wifi_networks(interface, fichier_base, duree):
    print(f"Recherche des réseaux Wi-Fi sur {interface} pendant {duree} secondes...")
    process = subprocess.Popen(
        ["sudo", "airodump-ng", "--write", fichier_base, interface],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE
    )
    time.sleep(duree)
    process.terminate()
    print(f"[SUCCESS] : La capture a été enregistrée")


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
def display_networks_and_select_target(reseaux, dossier_json):
    if not reseaux:
        print("Aucun réseau détecté.")
        return

    print("\nRéseaux Wi-Fi disponibles:")
    for idx, reseau in enumerate(reseaux, start=1):
        print(f"{idx}. BSSID: {reseau['BSSID']}, Channel: {reseau['Channel']}, Security: {reseau['Security']}, ESSID: {reseau['ESSID']}")

    while True:
        try:
            choice = int(input("\nChoisissez un réseau par son numéro : "))
            if 1 <= choice <= len(reseaux):
                target = reseaux[choice - 1]
                return target
            else:
                print("Veuillez entrer un numéro valide.")
        except ValueError:
            print("Veuillez entrer un nombre valide.")


# Supprime les fichiers de Capture
def clean_capture_directory():
    for fichier in os.listdir("Capture"):
        chemin_fichier = os.path.join("Capture", fichier)
        try:
            os.remove(chemin_fichier)
        except Exception as e:
            print(f"[ERREUR] Impossible de supprimer {chemin_fichier} : {e}")


# Supprime les fichiers de Result
def clean_result_directory():
    for fichier in os.listdir("Result"):
        chemin_fichier = os.path.join("Result", fichier)
        try:
            os.remove(chemin_fichier)
        except Exception as e:
            print(f"[ERREUR] Impossible de supprimer {chemin_fichier} : {e}")